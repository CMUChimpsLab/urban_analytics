#!/usr/bin/env python

# Pull tweets out of a collection in mongodb and put them into postgresql.
# Warning! This doesn't check if the tweets are already in there or not.
# So it may create duplicates.

import argparse, pymongo, psycopg2, sys, traceback

mongo_db = pymongo.MongoClient('localhost', 27017)['tweet']
psql_conn = psycopg2.connect("dbname='tweet' user='dantasse'")

cur = psql_conn.cursor()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', default='tweet_pgh')
    args = parser.parse_args()

    print "About to drop the table in postgres and reload it. Ok? (enter to continue, ctrl-c to quit."
    raw_input()

    cur.execute("DROP TABLE IF EXISTS tweet_pgh;")
    cur.execute("CREATE TABLE tweet_pgh(text VARCHAR(500), user_screen_name VARCHAR(50), created_at VARCHAR(100));");
    cur.execute("SELECT AddGeometryColumn('tweet_pgh', 'coordinates', 4326, 'POINT', 2)")
    counter = 0
    for tweet in mongo_db['tweet_pgh'].find():
        text = tweet['text']
        user_screen_name = tweet['user']['screen_name']
        lat = tweet['coordinates']['coordinates'][1]
        lon = tweet['coordinates']['coordinates'][0]
        created_at = tweet['created_at']

        try:
            sqlstr = "INSERT INTO tweet_pgh(text, user_screen_name, coordinates, created_at) VALUES ('%s', '%s', ST_SetSRID(ST_MakePoint(%s, %s), 4326), '%s')" %(text, user_screen_name, lon, lat, created_at)
            cur.execute("INSERT INTO tweet_pgh(text, user_screen_name, coordinates, created_at) VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)",(text, user_screen_name, lon, lat, created_at))
            psql_conn.commit()
        except Exception as e:
            print "Error on tweet from user " + user_screen_name
            traceback.print_exc()
            traceback.print_stack()

        counter += 1
        if counter % 1000 == 0:
            print str(counter) + " tweets entered"

    psql_conn.close()
