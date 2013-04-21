#!/usr/bin/env python2.7
# file: imgup.py

# simple anonymous photo upload to imgur (by default)
# returns the url for the image

import requests
import os
def get_cid():
    ''' wrap this so sloth_bot can access it'''
    path = os.path.join(os.path.expanduser('~'), '.imgur_client_id')
    with open(path) as fd:
        client_id = fd.read()
    return client_id

def upload_image(image, title):
    post_url = 'https://api.imgur.com/3/image.json'
    client_id = get_cid() #0# INSERT CLIENT ID
    res = requests.post(
        post_url,
        verify = False,
        params = {'type': 'file',
                  'title': title},
        files = {'image': image},
        headers= {'Authorization': "Client-ID " + client_id})
    j = res.json()

    if j['success']:
        url = 'http://imgur.com/' + j['data']['id']
        return url
    else:
        print 'status: {0}\nerror: {1}'.format(j['status'], j['data']['error'])
        return "oops, that sloth got away"
