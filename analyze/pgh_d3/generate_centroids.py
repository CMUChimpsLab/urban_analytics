#!/usr/bin/env python

# For each user who has tweeted at least once, find all their tweets (that are
# in Pittsburgh) and compute the centroid. Then add a row to the DB consisting
# of the user and their centroid.
#
# TODO: actually calculate centroid. Right now we're just using average lon/lat
# (which is okay for city-scale distances but not really accurate).

import pymongo

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']

# returns a set of all unique user ids
def find_all_user_ids():
    all_user_ids = []
    # use tweet_pgh_good, not tweet_pgh
    all_tweets = db.tweet_pgh_good.find()
    for tweet in all_tweets:
        all_user_ids.append(tweet['user']['id'])
    return set(all_user_ids)


def generate_centroids():
    user_ids = find_all_user_ids()
    print "got all user ids"
    counter = 0
    for user_id in user_ids:
        counter += 1
        if (counter % 1000) == 0:
            print counter
        # print user_id
        # use tweet_pgh_good, not tweet_pgh
        users_tweets = db.tweet_pgh_good.find({'user.id':user_id})
        users_tweets_coords = []
        for tweet in users_tweets:
            screen_name = tweet['user']['screen_name']
            if tweet['coordinates'] is not None:
                # print tweet['coordinates']
                users_tweets_coords.append(tweet['coordinates']['coordinates'])
        if len(users_tweets_coords) == 0:
            continue # they don't really have any lon/lat points
        user_lon = sum([point[0] for point in users_tweets_coords])/len(users_tweets_coords)
        user_lat = sum([point[1] for point in users_tweets_coords])/len(users_tweets_coords)

        user = {'_id': user_id, 'screen_name': screen_name, 'centroid': [user_lon, user_lat]} # TODO get screen name in there
        # print user
        cursor = db.user.find({'_id': user_id})
        if (cursor.count() > 0):
            db.user.update(cursor[0], user)
        else:
            db.user.insert(user)

if __name__ == '__main__':
    db.tweet_pgh_good.ensure_index("user.id")
    print "generating centroids now"
    generate_centroids()


