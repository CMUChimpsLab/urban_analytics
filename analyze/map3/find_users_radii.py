#!/usr/bin/env python

# For each user, find the radius within which 50% of their tweets fall.
# Same with 90%.

import pymongo, operator, math

db = pymongo.MongoClient('localhost', 27017)['tweet']

# returns a set of all unique user ids
def find_all_user_ids():
    all_user_ids = set()
    all_tweets = db.tweet_pgh.find()
    counter = 0
    for tweet in all_tweets:
        counter += 1
        if counter % 1000 == 0:
            print counter
        all_user_ids.add(tweet['user']['id'])
    return all_user_ids

# given two coordinates like [1, 4] and [5, 2]
def sum_coords(coords_1, coords_2):
    return [coords_1[0] + coords_2[0], coords_1[1] + coords_2[1]]

# distance between two points, each is [x, y]
def dist(c1, c2):
    return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2))


def generate_centroids_and_radii(user_ids):
    counter = 0
    for user_id in user_ids:
        counter += 1
        if counter % 1000 == 0:
            print 'users complete: ' + str(counter) 
        tweets = db.tweet_pgh.find({'user.id': user_id})
        
        coords = [tweet['coordinates']['coordinates'] for tweet in tweets]
        # flexing functional chops, not sure if this is even a good idea
        # basically I'm just averaging the xs and the ys.
        centroid = reduce(sum_coords, coords)
        centroid = [centroid[0] / len(coords), centroid[1] / len(coords)]

        coords.sort(key=lambda coord: dist(coord, centroid))
        fifty_pct_index = len(coords) / 2
        ninety_pct_index = len(coords) * 9 / 10
        fifty_pct_radius = dist(coords[fifty_pct_index], centroid)
        ninety_pct_radius = dist(coords[ninety_pct_index], centroid)
        
        screen_name = ''
        for tweet in tweets:
            screen_name = tweet['user']['screen_name']
        
        user = db.user.find_one({'_id': user_id})
        user['screen_name'] = screen_name
        user['centroid'] = centroid
        user['50%radius'] = fifty_pct_radius
        user['90%radius'] = ninety_pct_radius
        db.user.save(user)
        

if __name__ == '__main__':
    print 'getting user IDs'
    user_ids = find_all_user_ids()
    print 'done getting user IDs, generating centroids and radii'
    generate_centroids_and_radii(user_ids)
    print 'done'
    
