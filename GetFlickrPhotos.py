#!/usr/bin/env python

# Get all the flickr public photos that are geotagged in Pittsburgh.
# https://secure.flickr.com/services/api/flickr.photos.search.html

import requests, json, datetime, time, sys
from pymongo import Connection
db = Connection('localhost',27017)['flickr']

# don't check in API key
api_key = ''

mainParams = {'method':'flickr.photos.search',\
    'api_key': api_key,\
    'bbox':'-80.2,40.241667,-79.8,40.641667',\
    'format':'json',\
    'nojsoncallback':1}

infoParams = {'method':'flickr.photos.getInfo',\
    'api_key': api_key,\
    'photo_id': '',\
    'format':'json',\
    'nojsoncallback':1}

searchDate = datetime.datetime(2013, 8, 5)
# for some reason the flickr api isn't giving me any photos taken after 9/1/13.
# so let's start there and go backwards.

timestamp = time.time()
errFile = open('flickr_error_%d.log'%(timestamp), 'w')
outFile = open('flickr_output_%d.log'%(timestamp), 'w')
sys.stdout = outFile
sys.stderr = errFile

while True:
    mainParams['min_taken_date'] = str(searchDate)
    mainParams['max_taken_date'] = str(searchDate + datetime.timedelta(1)) # 1 day

    r = requests.get('http://api.flickr.com/services/rest/', params=mainParams)
    num_photos = int(r.json()['photos']['total'])
    print "Searched: %s, found this many photos: %s" % (mainParams['min_taken_date'], num_photos)
    if num_photos > 250:
        print "Warning: too many photos for this day. Number: %s" % num_photos

    for photo in r.json()['photos']['photo']:
        infoParams['photo_id'] = photo['id']
        rInfo = requests.get('http://api.flickr.com/services/rest/', params=infoParams)
        photoInfo = rInfo.json()
        photoInfo['_id'] = photo['id'] # so Mongo uses it as primary ID
        db.flickr_pgh.insert(dict(photoInfo))
        # print photo['id']

    searchDate -= datetime.timedelta(1)
    time.sleep(120)
    # no idea what the rate limit is, and 1 every 4 min ~ 1 year per day
    # so no need to get greedy.
    # (note that every photo requires an API call too, so this could make a
    # lot of calls)


