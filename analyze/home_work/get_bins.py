#!/usr/bin/env python

# For each user who answered our survey, gets a count of the bins that that
# user has tweeted in.
# For example, {(40.536, -79.958): 4, (40.329, -80.132): 2, ...}
# Saves it to the DB (user table)

import pymongo, csv, time
from collections import Counter

db = pymongo.MongoClient('localhost', 27017)['tweet']

def round_latlon(lat, lon):
    if not lat or not lon:
        return (None, None)
    return (round(float(lat), 3), round(float(lon), 3))
 
if __name__ == '__main__':

    for line in csv.DictReader(open('twitter_home_work_clean.csv', 'rU')):
        screen_name = line['screen_name']
        home_lat = line['home_lat']
        home_lon = line['home_lon']
        work1_lat = line['work1_lat']
        work1_lon = line['work1_lon']
        work2_lat = line['work2_lat']
        work2_lon = line['work2_lon']
        bins = Counter()
        tweets_cursor = db['tweet_pgh'].find({'user.screen_name':screen_name})
        for tweet in tweets_cursor:
            coords = tweet['coordinates']['coordinates']
            lon = coords[0]
            lat = coords[1]
            bins[round_latlon(lat, lon)] += 1
        print bins
        print 'home: %s' % str(round_latlon(home_lat, home_lon))
        print 'work1: %s' % str(round_latlon(work1_lat, work1_lon))
        print 'work2: %s' % str(round_latlon(work2_lat, work2_lon))
        print 

