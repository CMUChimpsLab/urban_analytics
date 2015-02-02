#!/usr/bin/env python

# Pull tweets out of a collection in mongodb and put them into postgresql.
# Warning! This doesn't check if the tweets are already in there or not.
# So it may create duplicates.

import argparse, pymongo, psycopg2

mongo_db = pymongo.MongoClient('localhost', 27017)['tweet']
psql_conn = psycopg2.connect("dbname='tweet' user='dtasse' host='localhost'")

cur = psql_conn.cursor()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', default='tweet_pgh')
    args = parser.parse_args()

    counter = 0
    for tweet in mongo_db['tweet_pgh'].find():
        text = tweet['text']
        user_screen_name = tweet['user']['screen_name']
        lat = tweet['coordinates']['coordinates'][1]
        lon = tweet['coordinates']['coordinates'][0]
        created_at = tweet['created_at']

        cur.execute("""INSERT INTO tweet_pgh(text, user_screen_name, coordinates, created_at)
            VALUES (%s, %s, Point(%s, %s), %s)  """, \
            (text, user_screen_name, lat, lon, created_at))
        psql_conn.commit()
        counter += 1
        if counter % 1000 == 0:
            print str(counter) + " tweets entered"

    psql_conn.close()
