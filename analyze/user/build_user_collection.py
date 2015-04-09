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

def load_nghds(json_file="neighborhoods.json"):
    neighborhoods = geojson.load(open(json_file))
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

 
def doAll():
    print "building indexes"
    db['tweet_pgh'].ensure_index('user.id')
    db['tweet_pgh'].ensure_index('user.screen_name')
    print "done, loading neighborhoods"
    global nghds # TODO ugh
    nghds = load_nghds()
    print "done"

    print "Getting user ids"
    user_screen_names = set()
    for tweet in db['tweet_pgh'].find():
        user_screen_names.add(tweet['user']['screen_name'])
        
    for user_screen_name in user_screen_names:
        user = db['user'].find_one({'screen_name': user_screen_name})
        if not user:
            user = {}
        try:
            tweets = db['tweet_pgh'].find({'user.screen_name':user_screen_name})
            tweets = list(tweets)
            user['screen_name'] = user_screen_name

            num_tweets = len(tweets)
            user['num_tweets'] = num_tweets

            centroid_radii = generate_centroids_and_radii(tweets)
            user.update(centroid_radii)

            user_nghds = get_user_nghds(tweets)
            user['neighborhoods'] = dict(user_nghds)
            if len(user_nghds) > 0:
                user['most_common_neighborhood'] = user_nghds.most_common(1)[0][0]
            else:
                user['most_common_neighborhood'] = 'Outside Pittsburgh'
                print 'Huh? User has zero tweets in neighborhoods?' + user_screen_name
            print user
            db.user.save(user)
        except Exception as e:
            print 'Exception.'
            print e

if __name__ == '__main__':
    # doAll()
    cProfile.run("doAll()")    
