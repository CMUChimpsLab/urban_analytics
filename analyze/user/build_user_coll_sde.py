#!/usr/bin/env python

# Builds up the "user" collection.
# Adds:
# - most common neighborhood
# - centroid (by averaging lat and lon)
# - 50% radius (half their tweets are inside this circle)
# - 90% radius (90% of their tweets are inside this circle)

import geojson, pymongo, collections, cProfile, math
from earth_distance import earth_delta_lat
import earth_distance

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']

def sum_coords(coords_1, coords_2):
    return [coords_1[0] + coords_2[0], coords_1[1] + coords_2[1]]

# distance between two points, each is [x, y], based on sphere earth
def dist(c1, c2):
    return earth_distance.earth_distance_m(c1[0], c1[1], c2[0], c2[1])
    # return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2))

# given one user's tweets, return the centroid and radii
def generate_centroids_and_sd(tweets):
    coords = []
    for tweet in tweets:
        if tweet and tweet['coordinates'] and tweet['coordinates']['coordinates']:
            coords += [tweet['coordinates']['coordinates']]

    if len(coords) == 0:
        print 'No coordinates'
        return {'centroid':None, 'sd_x':None, 'sd_y':None, 'angle':None}
    # flexing functional chops, not sure if this is even a good idea
    # basically I'm just averaging the xs and the ys.
    centroid = reduce(sum_coords, coords)
    centroid = [centroid[0] / len(coords), centroid[1] / len(coords)]

#    coords.sort(key=lambda coord: dist(coord, centroid))
    # http://resources.esri.com/help/9.3/ArcGISengine/java/Gp_ToolRef/spatial_statistics_tools/how_directional_distribution_colon_standard_deviational_ellipse_spatial_statistics_works.htm
    # http://onlinelibrary.wiley.com/store/10.1111/j.1538-4632.2002.tb01082.x/asset/j.1538-4632.2002.tb01082.x.pdf;jsessionid=36C968AA032165BEF026659D0D9E0E7B.f01t02?v=1&t=i3m3hyxt&s=48d9fe847096d8af0acc37302fd1780c12dab77e
    mean_x, mean_y = centroid
    N = len(coords)
    print coords
    print centroid
    delta_x = [earth_delta_lat(coord[0], mean_x) for coord in coords]
    delta_y = [earth_delta_lat(coord[1], mean_y) for coord in coords] # TODO: use earth_delta_long after fixing bug
    print delta_x, delta_y
    sum_delta_squares_x = sum([x ** 2 for x in delta_x])
    sum_delta_squares_y = sum([y ** 2 for y in delta_y])
    print sum_delta_squares_x, sum_delta_squares_y, N
    angle_A = sum_delta_squares_x - sum_delta_squares_y
    angle_B = (sum_delta_squares_x - sum_delta_squares_y) ** 2 + 4 * ((sum([delta_x[i] * delta_y[i] for i in range(0, N)])) ** 2)
    angle_B = math.sqrt(angle_B)
    angle_C = 2 * (sum([delta_x[i] * delta_y[i] for i in range(0, len(delta_x))]))
    print angle_A, angle_B, angle_C
    if angle_C == 0:
        angle = 0 # TODO: or pi/2 ...
    else:
        tan_theta = (angle_A + angle_B) / angle_C
        angle = math.atan(tan_theta)

    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    '''
    sd_x = [(delta_x[i] * cos_angle - delta_y[i] * sin_angle) ** 2 for i in range(0, N)]
    sd_y = [(delta_x[i] * sin_angle - delta_y[i] * cos_angle) ** 2 for i in range(0, N)]

    sd_x = math.sqrt(2 * sum(sd_x) / (N-2))
    sd_y = math.sqrt(2 * sum(sd_y) / (N-2))
    '''
    sum_xy = [delta_x[i] * delta_y[i] for i in range(0, N)]
    sum_xy = sum(sum_xy)
    sd_x = (cos_angle ** 2) * sum_delta_squares_x + (sin_angle ** 2) * sum_delta_squares_y + math.sin(2 * angle) * sum_xy
    sd_x = math.sqrt(sd_x / N)
    sd_y = (cos_angle ** 2) * sum_delta_squares_y + (sin_angle ** 2) * sum_delta_squares_x + math.sin(2 * angle) * sum_xy
    sd_y = math.sqrt(sd_y / N)
    print sd_x, sd_y, angle

    results = {}
    results['centroid'] = centroid
    results['sd_x'] = 2 * sd_x
    results['sd_y'] = 2 * sd_y
    results['angle'] = angle * 180 / math.pi
    return results

# If all tweets are from the same user, returns the screen name of that user.
# (don't call it if not all |tweets| are from the same user.)
def get_screen_name(tweets):
    for tweet in tweets:
        if tweet['user']['screen_name']:
            return tweet['user']['screen_name']
 
def doAll():
    print "building indexes"
    db['tweet_pgh'].ensure_index('user.id')

    user = db['user'].find({'_id': 2194548046})[0]
    tweets = db['tweet_pgh'].find({'user.id':2194548046})
    tweets = list(tweets)
    screen_name = get_screen_name(tweets)
    print "user: " + screen_name
    user['screen_name'] = screen_name

    num_tweets = len(tweets)
    user['num_tweets'] = num_tweets

    centroid_sd = generate_centroids_and_sd(tweets)
    user.update(centroid_sd)
    print user
    db.user.save(user)
    '''
    for user in db['user'].find().batch_size(100):
        tweets = db['tweet_pgh'].find({'user.id':user['_id']})
        tweets = list(tweets)
        screen_name = get_screen_name(tweets)
        print "user: " + screen_name
        user['screen_name'] = screen_name

        num_tweets = len(tweets)
        user['num_tweets'] = num_tweets

        centroid_sd = generate_centroids_and_sd(tweets)
        user.update(centroid_sd)
        print user
        db.user.save(user)
    '''

if __name__ == '__main__':
    doAll()
