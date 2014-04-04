#!/usr/bin/env python

# Takes all tweets from the tweet_pgh_good collection that are from Foursquare
# and copies them into another table called foursquare.

import pymongo

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']

def pick_out_4sq_tweets():
    # Find the tweets from Foursquare... TODO: is this the best way to find them?
    for tweet in db.tweet_pgh_good.find({'source':'<a href="http://foursquare.com" rel="nofollow">foursquare</a>'}):
        id = tweet['_id']
        db.foursquare.update({'_id':id}, tweet, upsert=True)

if __name__ == '__main__':
    print "copying all tweets from the tweet_pgh_good table that are from foursquare into the foursquare table"
    pick_out_4sq_tweets()
    print "done"

