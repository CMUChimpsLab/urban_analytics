#!/usr/bin/env python

# For each user in the database, adds what the most common neighborhood
# that they tweet in is.

import geojson
import shapely.geometry
import pymongo
import collections
import cProfile

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']
pittsburgh_outline = None

def load_nghds():
    neighborhoods = geojson.load(open('static/neighborhoods.json'))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    global pittsburgh_outline
    pittsburgh_outline = nghds[0]['shape']
    for nghd in nghds:
        pittsburgh_outline = pittsburgh_outline.union(nghd['shape'])
    return nghds
    # return [shapely.geometry.asShape(nghd) for nghd in neighborhoods['features']]

# this takes a lot of runtime.
def get_neighborhood_name(nghds, lon, lat):
    point = shapely.geometry.Point(lon, lat)
    global pittsburgh_outline # TODO ugh globals
    if not pittsburgh_outline.contains(point):
        return 'Outside Pittsburgh'
    
    for nghd in nghds:
        if nghd['shape'].contains(point):
            # Move this nghd to the front of the queue so it's checked first next time
            nghds.remove(nghd)
            nghds.insert(0, nghd)
            return nghd.properties['HOOD']
    return 'Outside Pittsburgh'


def doAll():
    print "building indexes"
    db['tweet_pgh'].ensure_index('user.id')
    print "done, loading neighborhoods"
    nghds = load_nghds()
    print "done"
    for user in db['user'].find().batch_size(100):
        print "user: " + str(user['screen_name'])
        tweets = db['tweet_pgh'].find({'user.id':user['_id']})
        print tweets.count()
        user_nghds = collections.Counter()
        for tweet in tweets:
            # print [n.properties['HOOD'] for n in nghds[0:5]]
            user_nghd_name = get_neighborhood_name(nghds,
                tweet['coordinates']['coordinates'][0],
                tweet['coordinates']['coordinates'][1])
            user_nghds[user_nghd_name] += 1
        
        if len(user_nghds) > 0:
            user['most_common_neighborhood'] = user_nghds.most_common(1)[0][0]
        else:
            user['most_common_neighborhood'] = 'Outside Pittsburgh'
        db['user'].save(user)
        print user['most_common_neighborhood']

    # for tweet in db['tweet_pgh'].find():
    #     print get_neighborhood_name(nghds,
    #         tweet['coordinates']['coordinates'][0],
    #         tweet['coordinates']['coordinates'][1])
if __name__ == '__main__':
    doAll()
    # cProfile.run("doAll()")    
