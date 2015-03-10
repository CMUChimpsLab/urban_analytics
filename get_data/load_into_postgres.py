#!/usr/bin/env python

# Drops any postgres table that already exists (!), recreates it, then 
# pull tweets out of a collection in mongodb and put them into postgresql.
# Warning! This doesn't check if the tweets are already in there or not.
# So it may create duplicates.

import argparse, pymongo, psycopg2, psycopg2.extensions, ppygis, traceback

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

mongo_db = pymongo.MongoClient('localhost', 27017)['tweet']
psql_conn = psycopg2.connect("dbname='tweet' user='dantasse'")

pg_cur = psql_conn.cursor()

def tweet_to_db_row(tweet):
    text = tweet['text']
    user_screen_name = tweet['user']['screen_name']
    lat = tweet['coordinates']['coordinates'][1]
    lon = tweet['coordinates']['coordinates'][0]
    created_at = tweet['created_at']
    insert_str = cur.mogrify("INSERT INTO tweet_pgh(text, user_screen_name, " +
            "coordinates, created_at)" + 
            "VALUES (%s, %s, Point(%s, %s), %s)  ", \
            (text, user_screen_name, lat, lon, created_at))
    return insert_str

    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', default='tweet_pgh')
    args = parser.parse_args()

    print "About to copy Mongo to Postgres. Enter to continue, Ctrl-C to quit."
    pg_cur.execute("DROP TABLE IF EXISTS tweet_pgh;")
    pg_cur.execute("""CREATE TABLE tweet_pgh(
        id integer primary key,
        favorite_count integer,
        lang string,
        created_at string,
        retweeted bool, 
        user_screen_name string NOT NULL,
        text string NOT NULL
        );""")
    cur.execute("SELECT AddGeometryColumn('tweet_pgh', 'coordinates', 4326, 'POINT', 2)")

    counter = 0
    for tweet in mongo_db['tweet_pgh'].find():
        insert_str = tweet_to_db_row(tweet)
        print insert_str
        try:
            cur.execute(insert_str)
            psql_conn.commit()
        except Exception as e:
            print "Error on tweet from user " + user_screen_name
            print "tweet name: %s, text: %s, lon=%d, lat=%d, created_at=%s" % (user_screen_name, text, lon, lat, created_at)
            # traceback.print_exc()
            # traceback.print_stack()
            psql_conn.commit()

        counter += 1
        if counter % 1000 == 0:
            print str(counter) + " tweets entered"

    psql_conn.close()
