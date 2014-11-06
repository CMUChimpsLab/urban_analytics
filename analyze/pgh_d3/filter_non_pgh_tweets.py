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


def remove_non_pgh_tweets():
    counter = 0
    for tweet in db.tweet_pgh.find():
        counter += 1
        if (counter % 1000 == 0):
            print counter
        if tweet['coordinates'] == None:
            print "delete, no coordinates"
            db.tweet_pgh.remove({'_id': tweet['_id']})
        else:
            lon = tweet['coordinates']['coordinates'][0]
            lat = tweet['coordinates']['coordinates'][1]
            if lon < MIN_LON or lon > MAX_LON:
                print "delete, bad longitude: " + str(lon)
                db.tweet_pgh.remove({'_id': tweet['_id']})
            elif lat < MIN_LAT or lat > MAX_LAT:
                print "delete, bad latitude: " + str(lat)
                db.tweet_pgh.remove({'_id': tweet['_id']})
            else:
                print "good: " + str(lon) + ", " + str(lat)

if __name__ == '__main__':
    print "About to remove all tweets not actually in Pittsburgh"
    print "that is, all tweets outside Lon %f to %f, and Lat %f to %f" % (MIN_LON, MAX_LON, MIN_LAT, MAX_LAT)
    print "Are you sure? ctrl-c if not."
    raw_input()
    print "count before: " + str(db.tweet_pgh.count())
    remove_non_pgh_tweets()
    
    print "count after: " + str(db.tweet_pgh.count())
    # print "ensuring indexes"
    # db['tweet_pgh_good'].ensure_index([('coordinates', pymongo.GEOSPHERE)])
    print "done"

