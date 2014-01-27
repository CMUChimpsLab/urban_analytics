#!/usr/bin/env python

# Get all the flickr public photos that are geotagged in Pittsburgh.
# Starts nearish to the present, goes backwards in time.
# https://secure.flickr.com/services/api/flickr.photos.search.html

import requests, json, datetime, time, sys, argparse
import pymongo

# don't check in API key
api_key = ''

parser = argparse.ArgumentParser()
parser.add_argument('--start_date',
                   help='latest date to search from. format YYYY-mm-dd',
                   default='2013-08-05')
# for some reason, flickr api isn't giving me any photos taken after 2013-8-5.
# so let's start there and go backwards.
args = parser.parse_args()
searchDate = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')

db = pymongo.Connection('localhost',27017)['flickr']

# Flickr API says you can go up to 500 photos at a time, but it appears to not
# actually honor this parameter if you set it to 500? ugh. 250 seems to work.
PER_PAGE = 250

mainParams = {'method':'flickr.photos.search',\
    'api_key': api_key,\
    'bbox':'-80.2,40.241667,-79.8,40.641667',\
    'per_page': PER_PAGE,\
    'format':'json',\
    'nojsoncallback':1}

infoParams = {'method':'flickr.photos.getInfo',\
    'api_key': api_key,\
    'photo_id': '',\
    'format':'json',\
    'nojsoncallback':1}

timestamp = time.time()
errFile = open('flickr_error_%d.log'%(timestamp), 'w')
outFile = open('flickr_output_%d.log'%(timestamp), 'w')
sys.stdout = outFile
sys.stderr = errFile

# given a list of unicode string IDs, request info on each one and store in db.
def get_these_photos(ids):
    for photo_id in ids:
        infoParams['photo_id'] = photo_id
        rInfo = requests.get('http://api.flickr.com/services/rest/', params=infoParams)
        photoInfo = rInfo.json()
        photoInfo['_id'] = photo['id'] # so Mongo uses it as primary ID
        db.flickr_pgh.insert(dict(photoInfo))

while True:
    mainParams['page'] = 1
    mainParams['min_taken_date'] = str(searchDate)
    mainParams['max_taken_date'] = str(searchDate + datetime.timedelta(1)) # 1 day

    r = requests.get('http://api.flickr.com/services/rest/', params=mainParams)
    num_photos = int(r.json()['photos']['total'])
    print "Searched: %s, found this many photos: %s" % (mainParams['min_taken_date'], num_photos)

    id_list = [photo['id'] for photo in r.json()['photos']['photo']]

    # catch extra pages if there are any
    num_pages = num_photos / PER_PAGE + 2 # PER_PAGE + 1 should work, but we
    # give it a little fudge factor because sometimes the count is off. worst
    # case, you do another request for a page number too high, and it returns
    # nothing.

    for page_num in range(2, num_pages + 1): # +1 because range is exclusive
        mainParams['page'] = page_num
        r2 = requests.get('http://api.flickr.com/services/rest/', params=mainParams)
        id_list += [photo['id'] for photo in r2.json()['photos']['photo']]
        print "Searched for another page, got this many photos now: %d" % len(id_list)

    id_list = list(set(id_list)) # remove duplicates due to paging weirdness
    get_these_photos(id_list)

    searchDate -= datetime.timedelta(1)
    time.sleep(120)
    # no idea what the rate limit is, and 1 every 4 min ~ 1 year per day
    # so no need to get greedy.
    # (note that every photo requires an API call too, so this could make a
    # lot of calls)


