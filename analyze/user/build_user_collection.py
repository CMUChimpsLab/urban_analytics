#!/usr/bin/env python

# Builds up the "user" collection.
# Adds:
# - most common neighborhood
# - centroid (by averaging lat and lon)
# - 50% radius (half their tweets are inside this circle)
# - 90% radius (90% of their tweets are inside this circle)

import geojson, shapely.geometry, pymongo, collections, cProfile
import earth_distance

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']
pittsburgh_outline = None # TODO ugh globals
nghds = None # TODO ugh again

def load_nghds():
    neighborhoods = geojson.load(open('neighborhoods.json'))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    global pittsburgh_outline # TODO ugh globals
    pittsburgh_outline = nghds[0]['shape']
    for nghd in nghds:
        pittsburgh_outline = pittsburgh_outline.union(nghd['shape'])
    return nghds
    # return [shapely.geometry.asShape(nghd) for nghd in neighborhoods['features']]

# Note: changes the order of |nghds|.
def get_neighborhood_name(nghds, lon, lat):
    point = shapely.geometry.Point(lon, lat)
    if not pittsburgh_outline.contains(point):# TODO ugh globals
        return 'Outside Pittsburgh'
    
    for nghd in nghds:
        if nghd['shape'].contains(point):
            # Move this nghd to the front of the queue so it's checked first next time
            nghds.remove(nghd)
            nghds.insert(0, nghd)
            nghd_name = nghd.properties['HOOD']
            return nghd_name.replace(".", "_") # for BSON; can't have .s in keys
    return 'Outside Pittsburgh'

def sum_coords(coords_1, coords_2):
    return [coords_1[0] + coords_2[0], coords_1[1] + coords_2[1]]

# distance between two points, each is [x, y], based on sphere earth
def dist(c1, c2):
    return earth_distance.earth_distance_m(c1[0], c1[1], c2[0], c2[1])
    # return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2))

# given one user's tweets, return the centroid and radii
def generate_centroids_and_radii(tweets):
    coords = [tweet['coordinates']['coordinates'] for tweet in tweets]
    if len(coords) == 0:
        print 'No coordinates'
        return {'centroid':None, '50%radius':None, '90%radius':None}
    # flexing functional chops, not sure if this is even a good idea
    # basically I'm just averaging the xs and the ys.
    centroid = reduce(sum_coords, coords)
    centroid = [centroid[0] / len(coords), centroid[1] / len(coords)]

    coords.sort(key=lambda coord: dist(coord, centroid))
    fifty_pct_index = len(coords) / 2
    ninety_pct_index = len(coords) * 9 / 10
    fifty_pct_radius = dist(coords[fifty_pct_index], centroid)
    ninety_pct_radius = dist(coords[ninety_pct_index], centroid)
    
    results = {}
    results['centroid'] = centroid
    results['50%radius'] = fifty_pct_radius
    results['90%radius'] = ninety_pct_radius
    return results

# Given one user's tweets, returns a Counter of neighborhood name -> number of
# times they tweeted in that neighborhood.
def get_user_nghds(tweets):
# Given one user's tweets, returns the name of their most common neighborhood.
# def get_most_common_nghd(tweets):
    user_nghds = collections.Counter()
    for tweet in tweets:
        # print [n.properties['HOOD'] for n in nghds[0:5]]
        user_nghd_name = get_neighborhood_name(nghds,
            tweet['coordinates']['coordinates'][0],
            tweet['coordinates']['coordinates'][1])
        user_nghds[user_nghd_name] += 1
    
    return user_nghds

# If all tweets are from the same user, returns the screen name of that user.
# (don't call it if not all |tweets| are from the same user.)
def get_screen_name(tweets):
    for tweet in tweets:
        if tweet['user']['screen_name']:
            return tweet['user']['screen_name']
 
def doAll():
    print "building indexes"
    db['tweet_pgh_good'].ensure_index('user.id')
    print "done, loading neighborhoods"
    global nghds # TODO ugh
    nghds = load_nghds()
    print "done"
    for user in db['user'].find().batch_size(100):
        tweets = db['tweet_pgh_good'].find({'user.id':user['_id']})
        tweets = list(tweets)
        screen_name = get_screen_name(tweets)
        print "user: " + screen_name
        user['screen_name'] = screen_name

        num_tweets = len(tweets)
        user['num_tweets'] = num_tweets

        centroid_radii = generate_centroids_and_radii(tweets)
        user.update(centroid_radii)

        user_nghds = get_user_nghds(tweets)
        user['neighborhoods'] = dict(user_nghds)
        user['most_common_neighborhood'] = user_nghds.most_common(1)[0][0]
        print user
        db.user.save(user)

if __name__ == '__main__':
    # doAll()
    cProfile.run("doAll()")    
