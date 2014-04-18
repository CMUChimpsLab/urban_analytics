#!/usr/bin/env python

# For each user in the database, adds what the most common neighborhood
# that they tweet in is.

import geojson
import shapely.geometry
import pymongo
import collections

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']

def load_nghds():
    neighborhoods = geojson.load(open('neighborhoods.json'))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    return nghds
    # return [shapely.geometry.asShape(nghd) for nghd in neighborhoods['features']]

def get_neighborhood_name(nghds, lon, lat):
    point = shapely.geometry.Point(lon, lat)
    for nghd in nghds:
        if nghd['shape'].contains(point):
            return nghd.properties['HOOD']
    return 'Outside Pittsburgh'

if __name__ == '__main__':
    nghds = load_nghds()
    for user in db['user'].find():
        tweets = db['tweet_pgh_good'].find({'user.id':user['_id']})
        user_nghds = collections.Counter()
        for tweet in tweets:
            user_nghd_name = get_neighborhood_name(nghds,
                tweet['coordinates']['coordinates'][0],
                tweet['coordinates']['coordinates'][1])
            user_nghds[user_nghd_name] += 1
        
        user['most_common_neighborhood'] = user_nghds.most_common(1)[0][0]
        db['user'].save(user)
        print user_nghds.most_common(1)[0][0]

    # for tweet in db['tweet_pgh_good'].find():
    #     print get_neighborhood_name(nghds,
    #         tweet['coordinates']['coordinates'][0],
    #         tweet['coordinates']['coordinates'][1])
