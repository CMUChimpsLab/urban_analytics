#!/usr/bin/env python

# Drops any postgres table that already exists (!), recreates it, then 
# pull tweets out of a collection in mongodb and put them into postgresql.
# Warning! This doesn't check if the tweets are already in there or not.
# So it may create duplicates.

import argparse, pymongo, psycopg2, psycopg2.extensions, ppygis, traceback
import pytz, datetime

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

mongo_db = pymongo.MongoClient('localhost', 27017)['tweet']
psql_conn = psycopg2.connect("dbname='tweet'")

pg_cur = psql_conn.cursor()

month_map = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 
    'Aug':8,  'Sep': 9, 'Oct':10, 'Nov': 11, 'Dec': 12}
# Special case date parsing. All our dates are like this:
# Wed Jan 22 23:19:19 +0000 2014
# 012345678901234567890123456789
# so let's just parse them like that. 
def parse_date(d):
    return datetime.datetime(int(d[26:30]), month_map[d[4:7]], int(d[8:10]),\
        int(d[11:13]), int(d[14:16]), int(d[17:19]), 0, pytz.timezone('UTC')) # 0=usec

# Map of field name -> postgres datatype. Contains everything we want to save.
# TODO: if you change this, also change the tweet_to_insert_string method below.
data_types = {
    # _id skipped; id (no underscore) works well enough for us.
    # 'contributors': 'ARRAY', # TODO does this work?
    'coordinates': 'Point',
    'created_at': 'timestamp',
    # 'entities': 'hstore', # TODO this is tricky too.
    'favorite_count': 'integer',
    # |favorited| only makes sense if there's an authenticated user.
    'filter_level': 'text',
    # geo skipped, b/c it's deprecated
    'lang': 'text',
    'id': 'bigint primary key',
    # id_str skipped; same as ID.
    'in_reply_to_screen_name': 'text',
    'in_reply_to_status_id': 'bigint',
    'in_reply_to_status_id_str': 'text',
    'in_reply_to_user_id': 'bigint',
    'in_reply_to_user_id_str': 'text',
    # 'place': 'hstore', # TODO this is tricky.
    'retweet_count': 'integer',
    # |retweeted| only make sense if there's an authenticated user.
    'source': 'text',
    'text': 'text NOT NULL',
    # truncated is obsolete; Twitter now rejects long tweets instead of truncating.
    # 'user': 'hstore', # TODO this may be tricky.
    'user_screen_name': 'text NOT NULL', # added this
}
    
# Argument: a tweet JSON object. Returns: a string starting with "INSERT..."
# that you can run to insert this tweet into a Postgres database.
def tweet_to_insert_string(tweet):
    lat = tweet['coordinates']['coordinates'][1]
    lon = tweet['coordinates']['coordinates'][0]
    coordinates = ppygis.Point(lon, lat, srid=4326)
    created_at = parse_date(tweet['created_at'])

    insert_str = pg_cur.mogrify("INSERT INTO tweet_pgh(" +
            "coordinates, created_at, favorite_count, filter_level, " +
            "lang, id, in_reply_to_screen_name, in_reply_to_status_id, " +
            "in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str, " +
            "retweet_count, source, text, user_screen_name) " + 
            "VALUES (" + ','.join(['%s' for key in data_types]) + ")", 
        (coordinates, created_at, tweet['favorite_count'], 
        tweet['filter_level'], tweet['lang'], tweet['id'],
        tweet['in_reply_to_screen_name'], tweet['in_reply_to_status_id'],
        tweet['in_reply_to_status_id_str'], tweet['in_reply_to_user_id'],
        tweet['in_reply_to_user_id_str'], tweet['retweet_count'],
        tweet['source'], tweet['text'],
        tweet['user']['screen_name']))
    return insert_str

    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', default='tweet_pgh')
    args = parser.parse_args()

    print "About to copy Mongo to Postgres. Enter to continue, Ctrl-C to quit."
    raw_input()
    pg_cur.execute("DROP TABLE IF EXISTS tweet_pgh;")
    psql_conn.commit()
    create_table_str = "CREATE TABLE tweet_pgh("
    for key, value in sorted(data_types.iteritems()):
        if key not in ['coordinates']: # create that coords column separately.
            create_table_str += key + ' ' + value + ', '
    create_table_str = create_table_str[:-2] + ");"

    pg_cur.execute(create_table_str)
    psql_conn.commit()
    pg_cur.execute("SELECT AddGeometryColumn('tweet_pgh', 'coordinates', 4326, 'POINT', 2)")
    psql_conn.commit()

    counter = 0
    for tweet in mongo_db['tweet_pgh'].find():
        insert_str = tweet_to_insert_string(tweet)
        try:
            pg_cur.execute(insert_str)
            psql_conn.commit()
        except Exception as e:
            print "Error running this command: %s" % insert_str
            traceback.print_exc()
            traceback.print_stack()
            psql_conn.commit()

        counter += 1
        if counter % 1000 == 0:
            print str(counter) + " tweets entered"

    psql_conn.close()
