#!/usr/bin/env python

# Utilities to take a JSON instagram and turn it into a PostgreSQL string that can
# then be run to insert it into Postgres.
#
# If run on its own, this file will:
# Drop any postgres table that already exists (!), recreate it, then 
# pull instagrams out of a collection in mongodb and put them into postgresql.

import argparse, pymongo, psycopg2, psycopg2.extras, psycopg2.extensions
import ppygis, traceback, pytz, datetime, send_email

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

mongo_db = pymongo.MongoClient('localhost', 27017)['instagram']
psql_conn = psycopg2.connect("dbname='tweet'")
psycopg2.extras.register_hstore(psql_conn)

pg_cur = psql_conn.cursor()

# Map of field name -> postgres datatype. Contains everything we want to save.
# TODO: if you change this, also change the instagram_to_insert_string method below.
data_types = {
    # |attribution| dropped
    'caption_from_username': 'text',
    'caption_id': 'bigint',
    'caption_text': 'text', # ignoring the rest of the caption
    'comments_count': 'integer', # ignoring the contents of the comments
    'created_time': 'timestamp',
    'filter': 'text',
    'id': 'text primary key', # copied from mongo instagram
    'image_standard_res_url': 'text', # ignoring the rest of the image
    'likes_count': 'integer', # ignoring who the likes are from
    'link': 'text',
    'location': 'Point',
    'tags': 'text[]', # hashtags.
    'type': 'text',
    'instagram_user': 'hstore', # was |user| in Instagram API.
    'user_username': 'text NOT NULL', # added this, redundant with instagram_user
    'user_id': 'bigint', # added this, redundant with instagram_user
    # ignoring users_in_photo
}

# Argument: a python dictionary. Returns: the same thing with all keys and
# values as strings, so we can make a postgres hstore with them.
def make_hstore(py_dict):
    if not py_dict:
        py_dict={}
    return {unicode(k): unicode(v) for k, v in py_dict.iteritems()}

# Argument: an instagram JSON object and a collection string name to insert into.
# Returns: a string starting with "INSERT..." that you can run to insert this
# instagram into a Postgres database.
def instagram_to_insert_string(instagram, collection):
    if instagram['caption'] != None:
        caption_from_username = instagram['caption']['from']['username']
        caption_id = int(instagram['caption']['id'])
        caption_text = instagram['caption']['text']
    else:
        caption_from_username = caption_id = caption_text = None
    comments_count = instagram['comments']['count']
    created_time = datetime.datetime.fromtimestamp(int(instagram['created_time']))

    filter = instagram['filter']
    id = instagram['_id']
    image_standard_res_url = instagram['images']['standard_resolution']['url']
    likes_count = instagram['likes']['count']
    link = instagram['link']

    lat = float(instagram['location']['latitude'])
    lon = float(instagram['location']['longitude'])
    location = ppygis.Point(lon, lat, srid=4326)

    tags = instagram['tags']
    type = instagram['type']
    instagram_user = make_hstore(instagram['user'])
    user_username = instagram['user']['username']
    user_id = int(instagram['user']['id'])

    insert_str = pg_cur.mogrify("INSERT INTO " + collection + "(caption_from_username," +
            "caption_id, caption_text, comments_count, created_time, filter, id," +
            "image_standard_res_url, likes_count, link, location, tags, type," +
            "instagram_user, user_username, user_id) " +
            "VALUES (" + ','.join(['%s' for key in data_types]) + ")", 
        (caption_from_username, caption_id, caption_text, comments_count,
        created_time, filter, id, image_standard_res_url, likes_count, link,
        location, tags, type, instagram_user, user_username, user_id))
    return insert_str

    
# TODO translate the rest of this function, I think I've got instagram-to-string done.
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', default='instagram_pgh')
    parser.add_argument('--recreate_table', '-r', action='store_true')
    args = parser.parse_args()

    if args.recreate_table:
        print "About to dump and recreate Postgres table. Enter to continue, Ctrl-C to quit."
        raw_input()
        pg_cur.execute("DROP TABLE IF EXISTS " + args.collection + ";")
        psql_conn.commit()
        create_table_str = "CREATE TABLE " + args.collection + "("
        for key, value in sorted(data_types.iteritems()):
            if key not in ['location']: # create that coords column separately.
                create_table_str += key + ' ' + value + ', '
        create_table_str = create_table_str[:-2] + ");"

        pg_cur.execute(create_table_str)
        psql_conn.commit()
        pg_cur.execute("SELECT AddGeometryColumn('" + args.collection + "', 'location', 4326, 'POINT', 2)")
        psql_conn.commit()
        # TODO does this create the indices?
        print "Done creating table, now creating indices"
        create_index_str = 'CREATE INDEX %s_user_username_match ON %s USING HASH(user_username);' % (args.collection, args.collection)
        vacuum_str = 'VACUUM ANALYZE %s;' % args.collection
        psql_conn.set_isolation_level(0) # so we can VACUUM outside a transaction
        pg_cur.execute(create_index_str)
        pg_cur.execute(vacuum_str)
        coordinates_geo_index_str = 'CREATE INDEX %s_location_geo ON %s USING GIST(location);' % (args.collection, args.collection)
        pg_cur.execute(coordinates_geo_index_str)
        pg_cur.execute(vacuum_str)
        psql_conn.set_isolation_level(1)
        print "Done creating indices"

    counter = 0
    for instagram in mongo_db[args.collection].find():
        if instagram['location'] == None:
            continue # only a couple that somehow have no locations

        insert_str = instagram_to_insert_string(instagram, args.collection)
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
            print str(counter) + " instagrams entered"

    psql_conn.close()
    send_email.send_dan_email('loading into %s is done!' % args.collection, 'yep sure is')

