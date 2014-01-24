#!/usr/bin/env python

# Get all the flickr public photos that are geotagged.

# https://secure.flickr.com/services/api/flickr.photos.search.html
# flickr.photos.search
# params:
# api_key: my API key
# min_taken_date: as mysql datetime or unix timestamp
# bbox: min_long, min_lat, max_long, max_lat

import requests, json
from pymongo import Connection
db = Connection('localhost',27017)['flickr']

# don't check in API key
api_key = ''

mainParams = {'method':'flickr.photos.search',\
    'api_key': api_key,\
    'min_taken_date': 1390595692,\
    'bbox':'-80.2,40.241667,-79.8,40.641667',\
    'format':'json',\
    'nojsoncallback':1}

r = requests.get('http://api.flickr.com/services/rest/', params=mainParams)

infoParams = {'method':'flickr.photos.getInfo',\
    'api_key': api_key,\
    'photo_id': '',\
    'format':'json',\
    'nojsoncallback':1}

for photo in r.json()['photos']['photo']:
    infoParams['photo_id'] = photo['id']
    rInfo = requests.get('http://api.flickr.com/services/rest/', params=infoParams)
    photoInfo = rInfo.json()
    photoInfo['_id'] = photoInfo['id'] # so Mongo uses it as primary ID
    del photoInfo['id']
    db.flickr_pgh.insert(dict(photoInfo))

# TODO wrap this in a loop
