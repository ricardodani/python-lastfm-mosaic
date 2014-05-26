# -*- coding: utf-8 -*-

import uuid
import lastfmapi
import memcache
from django.conf import settings
from cStringIO import StringIO
from octopus import TornadoOctopus
from PIL import Image


def _get_user_top_albums_response(**kwargs):
    '''Returns the response of the api album.getTopAlbums call
    '''
    mc = memcache.Client([settings.MEMCACHE_ADDRESS], debug=0)
    api = lastfmapi.LastFmApi(settings.LASTFM_API_KEY)

    cache_key = 'UsTopAlb|{user}|{period}'.format(**kwargs)

    res = mc.get(cache_key)
    if not res:
        res = api.user_getTopAlbums(**kwargs)['topalbums']['album']
        mc.set(cache_key, res)
    return res


def get_user_top_albums_images(user, period, limit, thumb_size):
    '''Returns images urls of the user top albums response
    '''
    IMAGE_SIZES = {
        "small": 0,
        "medium": 1,
        "large": 2,
        "extralarge": 3
    }

    def get_img(album, thumb_size=thumb_size):
        return album['image'][IMAGE_SIZES[thumb_size]]['#text']

    images_url = _get_user_top_albums_response(
        user=user, period=period, limit=limit * 1.2)
    return filter(lambda x: 'default_album_medium.png' not in x,
                  map(get_img, images_url))[:limit]


def _download_url_list(image_url_list):
    '''Downloads the image sources of images listed on `image_url_list`
    '''

    images = []

    otto = TornadoOctopus(
        concurrency=50, auto_start=True, cache=True, expiration_in_seconds=60
    )

    handle_url_response = lambda url, response: images.append(response.text)
    for url in image_url_list:
        otto.enqueue(url, handle_url_response)

    otto.wait(0)

    return images


def create_image_mosaic(image_url_list, width=1260, height=800):
    '''Download and manipulates the images of `image_url_list`
    to creates a mosaic with them
    '''

    images = _download_url_list(image_url_list)

    out_img = Image.new('RGB', (width, height))
    x, y = 0, 0

    for i, img in enumerate(images):
        thumb = Image.open(StringIO(img))
        out_img.paste(thumb, (y * thumb.size[0], x * thumb.size[1]))
        if (i + 1) % (width / thumb.size[0]) == 0:
            x += 1
            y = 0
        else:
            y += 1

    image_location = 'static/mosaics/%s.png' % uuid.uuid4()
    out_img.save(image_location)
    return image_location
