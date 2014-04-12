# -*- coding: utf-8 -*-

import lastfmapi
import memcache
from cStringIO import StringIO
from octopus import TornadoOctopus
from PIL import Image


LASTFM_API_KEY = 'c971171e6f5976ddae7717ce53ea2ee6'
MEMCACHE_ADDRESS = '127.0.0.1:11211'

mc = memcache.Client([MEMCACHE_ADDRESS], debug=0)
api = lastfmapi.LastFmApi(LASTFM_API_KEY)

images = []


def _get_user_top_albums_response(**kwargs):
    '''Returns the response of the api album.getTopAlbums call
    '''

    cache_key = 'UsTopAlb|{user}|{period}'.format(**kwargs)

    res = mc.get(cache_key)
    if not res:
        res = api.user_getTopAlbums(**kwargs)['topalbums']['album']
        mc.set(cache_key, res)
    return res


def get_user_top_albums_images(user, period='overall'):
    '''Returns images urls of the user top albums response
    '''

    def get_img(album):
        # image qualities -> 0 - 3
        return album['image'][2]['#text']

    images_url = _get_user_top_albums_response(
        user=user, period=period, limit=60)
    return filter(lambda x: 'default_album_medium.png' not in x,
                  map(get_img, images_url))[:50]


def create_image_mosaic(image_url_list):
    '''Saves a mosaic image with the images the given urls.
    '''

    otto = TornadoOctopus(
        concurrency=50, auto_start=True, cache=True, expiration_in_seconds=60
    )

    for url in image_url_list:
        otto.enqueue(url, handle_url_response)

    otto.wait(0)

    out_img = Image.new('RGB', (1260, 1260 / 2))
    x, y = 0, 0

    for i, img in enumerate(images):
        alb = Image.open(StringIO(img))
        out_img .paste(alb, (y * 126, x * 126))
        if (i + 1) % 10 == 0:
            x += 1
            y = 0
        else:
            y += 1

    out_img .save('mosaic.png')


def handle_url_response(url, response):
    images.append(response.content)
