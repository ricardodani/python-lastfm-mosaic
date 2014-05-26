# -*- coding: utf-8 -*-

import requests
import hmac
import json
import hashlib

GROOVESHARK_API_KEY = 'fb_coverart'
GROOVESHARK_API_SECRET = '58c8416d0f3735506af19e655213fd46'
GROOVESHARK_API_URL = "http://api.grooveshark.com/ws3.php?sig={}"


class GroovesharkApi(object):
    '''Grooveshark Api wrapper class
    '''

    # Consuming and Contributing to User Data (Sessions and User Authentication)

    # To modify and access user data an authenticated session is required. To
    # create a session, invoke startSession with your web services key and
    # signature. You will be returned an anonymous, unauthenticated session.
    # To then authenticate this session, invoke authenticateUser providing
    # sessionID, the user's lower-cased username and a token for that user.
    # The token is formed as md5(lowercase(username) + md5(password)).
    # Assuming the user has provided their correct username and password to
    # you, you will then have an authenticated session. You can then pass
    # this sessionID to methods like addUserFavoriteSong.

    def make_call(self, method, params=None):
        payload = {
            'method': method,
            'header': {
                'wsKey': GROOVESHARK_API_KEY
            }
        }
        if params:
            payload.update({'params': params})

        payloads = json.dumps(payload)
        url = GROOVESHARK_API_URL.format(self.message_signature(payloads))
        return requests.post(url, payloads)

    def message_signature(self, params):
        #return hash_hmac('md5', $params, $secret)
        hmac_hash = hmac.new(GROOVESHARK_API_SECRET, params, hashlib.md5)
        return hmac.hexdigest()

if __name__ == '__main__':
    gs = GroovesharkApi()
    r = gs.make_call('startSession')
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
