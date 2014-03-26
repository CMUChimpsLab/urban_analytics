#!/usr/bin/env python

# For each tweet, if it has a Coordinates field, save it in the "good" tweets
# collection. (sometimes the Twitter API gives us some without coordinates
# because the place.bounding_box field overlaps with Pittsburgh.

MIN_LON = -80.2
MAX_LON = -79.8
MIN_LAT = 40.241667
MAX_LAT = 40.641667

import pymongo

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']


def filter_non_pgh_tweets():
    counter = 0
    for tweet in db.tweet_pgh.find():
	counter += 1
	if (counter % 1000 == 0):
		print counter
        if tweet['coordinates'] is not None:
            
            lon = tweet['coordinates']['coordinates'][0]
            lat = tweet['coordinates']['coordinates'][1]
            if lon < MIN_LON or lon > MAX_LON:
		pass
            elif lat < MIN_LAT or lat > MAX_LAT:
                pass
            else:
                # this is an upsert: inserts if it's not already there
                db.tweet_pgh_good.update({'_id':tweet['_id']}, tweet, upsert=True)
        else:
            pass

if __name__ == '__main__':
    filter_non_pgh_tweets()



