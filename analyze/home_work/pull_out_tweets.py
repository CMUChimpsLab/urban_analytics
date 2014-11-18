#!/usr/bin/env python

# Gets all the tweets from the database that belong to the users in our clean
# data set. Dumps them out to tweets.json.

import csv, pymongo, json

dbclient = pymongo.MongoClient('localhost', 27017)
db = dbclient['tweet']
outfile = open('tweets.json', 'w')

if __name__ == '__main__':
    # I love python.
    all_tweeters = {line[1].lower():line[1] for line in csv.reader(open('common_tweeters.csv'))}

    clean_data =  csv.reader(open('twitter_home_work_clean.csv', 'rU'))
    next(clean_data) # skip headers
    all_tweets = []

    for line in clean_data:
        screen_name = all_tweeters[line[1].lower()] # all_tweeters to fix capitalization
        for tweet in db.tweet_pgh.find({'user.screen_name': screen_name}):
            del tweet['_id'] # ObjectId, not serializable.
            all_tweets.append(tweet)

    json.dump(all_tweets, outfile)
