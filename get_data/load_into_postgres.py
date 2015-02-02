#!/usr/bin/env python

# Pull tweets out of a collection in mongodb and put them into postgresql.

import argparse, pymongo

mongo_db = pymongo.MongoClient('localhost', 27017)['tweet']

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', default='tweet_pgh')
    args = parser.parse_args()

    for tweet in mongo_db['tweet_pgh'].find():
        print tweet
