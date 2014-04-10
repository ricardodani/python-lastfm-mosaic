# -*- coding: utf-8 -*-

import lastfmapi
import memcache

LASTFM_API_KEY = 'c971171e6f5976ddae7717ce53ea2ee6'
MEMCACHE_ADDRESS = '127.0.0.1:11211'

mc = memcache.Client([MEMCACHE_ADDRESS], debug=0)
api = lastfmapi.LastFmApi(LASTFM_API_KEY)


def _get_user_top_albums_response(**kwargs):
    '''Returns the response of the api album.getTopAlbums call
    '''

    cache_key = 'topalbums|{user}|{period}'.format(**kwargs)

    res = mc.get(cache_key)
    if not res:
        res = api.user_getTopAlbums(**kwargs)['topalbums']['album'][:50]
        mc.set(cache_key, res)
    return res


def get_user_top_albums_images(user, period='overall'):
    '''Returns images urls of the user top albums response
    '''

    def get_img(album):
        # image qualities -> 0 - 3
        return album['image'][2]['#text']

    return map(get_img,
               _get_user_top_albums_response(user=user, period=period))

# available periods: overall (default) | 7day | 1month | 3month | 6month | 12month
# just pass in second argument
print get_user_top_albums_images('ricardodani', '1month')
