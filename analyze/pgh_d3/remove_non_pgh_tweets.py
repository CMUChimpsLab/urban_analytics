#!/usr/bin/env python

# This script has been run already, and should not be necessary to run again.
# Our Twitter_stream.py now only saves "good" tweets.

# Anyway, what this script *did*: delete any tweet in the tweet_pgh collection
# that is not actually in Pittsburgh. (sometimes these would be there because
# the twitter API would give us stuff where the actual location is uncertain,
# but there's a bounding box that includes Pittsburgh.)

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
    print "done"

