# -*- coding: utf-8 -*-

import io
import lastfmapi
import memcache
import requests
from PIL import Image

LASTFM_API_KEY = 'c971171e6f5976ddae7717ce53ea2ee6'
MEMCACHE_ADDRESS = '127.0.0.1:11211'

mc = memcache.Client([MEMCACHE_ADDRESS], debug=0)
api = lastfmapi.LastFmApi(LASTFM_API_KEY)


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
    img = Image.new('RGB', (1260, 1260 / 2))
    x, y = 0, 0
    for i, url in enumerate(image_url_list):
        res = requests.get(url)
        stream = io.BytesIO(res.content)
        alb = Image.open(stream)
        img.paste(alb, (y * 126, x * 126))
        if (i + 1) % 10 == 0:
            x += 1
            y = 0
        else:
            y += 1
    img.save('mosaic.png')

# available periods: overall | 7day | 1month | 3month | 6month | 12month
create_image_mosaic(get_user_top_albums_images('ricardodani', '6month'))
