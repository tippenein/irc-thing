#!/usr/bin/python2.7

#file: geef_random.py

import re
import random
import urllib2
import simplejson as json
import HTMLParser
import imgup

api_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=define:'
DICT = '/usr/share/dict/words'

referer = 'irc-thing'

def random_definition():
    with open(DICT) as fd:
        word = random.choice(fd.read().splitlines())

    url = api_url + word
    request = urllib2.Request(url, None, {'Referer': referer})
    response = urllib2.urlopen(request)

    # Get JSON result
    results = json.load(response)
    data = results['responseData']
    dataInfo = data['results'][0]
    text = dataInfo['title'].split(' - ')[0] + ": "+ dataInfo['content']
    htmlparser = HTMLParser.HTMLParser()
    s = unicode(re.sub(r'<[^>]*?>', '', text))  #destroy all <tag>
    escaped = htmlparser.unescape(s)
    return unicode(escaped)

def geef_happiness():
    searchTerms = ["sloth","koala","wombat","bunny"]
    searchTerm = random.choice(searchTerms)
    # escape spaces
    searchTerm = searchTerm.replace(' ','%20')

    # Choose random start page. Images are retrieved in groups of 4
    sloth_start = random.randint(0, 15)
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(sloth_start*4))
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)

    # Get JSON result
    results = json.load(response)
    data = results['responseData']
    dataInfo = data['results']

    # Choose a random image from the result group
    result_size = len(dataInfo)
    imgurl = dataInfo[random.randint(0, result_size-1)]['unescapedUrl']

    img = urllib2.urlopen(imgurl)
    url = imgup.upload_sloth(img)

    return url

if __name__ == '__main__':
    print random_definition()
