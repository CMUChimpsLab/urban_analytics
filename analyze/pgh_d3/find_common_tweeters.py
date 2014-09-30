#!/usr/bin/env python

# Find all tweeters who have tweeted a lot, and how many times they've tweeted.
# TODO make this happen along with generate_centroids; no reason to do this twice really.
# Run once on 2014-09-29, tweaked it manually and ended up with common_tweeters.csv

import pymongo


dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']

# returns a set of all unique user ids
def find_all_user_ids():
    all_user_ids = []
    # use tweet_pgh_good, not tweet_pgh
    all_tweets = db.tweet_pgh_good.find()
    counter = 0
    for tweet in all_tweets:
        counter += 1
        if counter % 1000 == 0:
            print counter
        all_user_ids.append(tweet['user']['id'])
    return set(all_user_ids)


def find_frequent_tweeters():
    user_ids = find_all_user_ids()
    print "got all user ids, this many: %d" % len(user_ids)
    counter = 0
    for user_id in user_ids:
         
        # counter += 1
        # if (counter % 1000) == 0:
        #     print counter
        # use tweet_pgh_good, not tweet_pgh
        users_tweets = list(db.tweet_pgh_good.find({'user.id':user_id}))
        screen_name = users_tweets[0]['user']['screen_name']
        user = {'_id': user_id, 'screen_name': screen_name, 'num_tweets': len(users_tweets)}
        # TODO oops this wipes out whatever the user already had, like centroid, oops
        db.user.update({'_id': user_id}, user, upsert=True)

        print "%s,%s,%s" % (user_id, screen_name, len(users_tweets))

if __name__ == '__main__':
    print "finding frequent tweeters"
    find_frequent_tweeters()
    print "creating indexes"
    db['user'].ensure_index('_id')
    print "done"


