# -*- coding: utf-8 -*-

import lastfmapi
import memcache

from django.conf import settings


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
