#!/usr/bin/env python

# Builds up the "user" collection.
# Adds:
# - most common neighborhood
# - centroid (by averaging lat and lon)
# - 50% radius (half their tweets are inside this circle)
# - 90% radius (90% of their tweets are inside this circle)

import geojson, shapely.geometry, collections, cProfile, json
import earth_distance
import psycopg2, psycopg2.extras, ppygis

pittsburgh_outline = None # TODO ugh globals
nghds = None # TODO ugh again
psql_conn = psycopg2.connect("dbname='tweet'")
psycopg2.extras.register_hstore(psql_conn)
pg_cur = psql_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Argument: a python dictionary. Returns: the same thing with all keys and
# values as strings, so we can make a postgres hstore with them.
def make_hstore(py_dict):
    if not py_dict:
        py_dict={}
    return {unicode(k): unicode(v) for k, v in py_dict.iteritems()}

def load_nghds(json_file="neighborhoods.json"):
    neighborhoods = geojson.load(open(json_file))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    global pittsburgh_outline # TODO ugh globals
    pittsburgh_outline = nghds[0]['shape']
    for nghd in nghds:
        pittsburgh_outline = pittsburgh_outline.union(nghd['shape'])
    return nghds

# Note: changes the order of |nghds|.
def get_neighborhood_name(nghds, lon, lat):
    point = shapely.geometry.Point(lon, lat)
    if not pittsburgh_outline.contains(point):# TODO ugh globals
        return 'Outside Pittsburgh'
    
    for nghd in nghds:
        if nghd['shape'].contains(point):
            # Move this nghd to the front of the queue so it's checked first next time
            nghds.remove(nghd)
            nghds.insert(0, nghd)
            nghd_name = nghd.properties['HOOD']
            return nghd_name.replace(".", "_") # for BSON; can't have .s in keys
    return 'Outside Pittsburgh'

def sum_coords(coords_1, coords_2):
    return [coords_1[0] + coords_2[0], coords_1[1] + coords_2[1]]

# distance between two points, each is [x, y], based on sphere earth
def dist(c1, c2):
    return earth_distance.earth_distance_m(c1[0], c1[1], c2[0], c2[1])

# given one user's tweets, return the centroid and radii
def generate_centroids_and_radii(tweets):
    coords = [tweet['coordinates'] for tweet in tweets]
    if len(coords) == 0:
        print 'No coordinates'
        return {'centroid':None, '50%radius':None, '90%radius':None}
    centroid = reduce(sum_coords, coords)
    centroid = [centroid[0] / len(coords), centroid[1] / len(coords)]
 
    coords.sort(key=lambda coord: dist(coord, centroid))
    fifty_pct_index = len(coords) / 2
    ninety_pct_index = len(coords) * 9 / 10
    fifty_pct_radius = dist(coords[fifty_pct_index], centroid)
    ninety_pct_radius = dist(coords[ninety_pct_index], centroid)
 
    results = {}
    results['centroid'] = centroid
    results['pct50_radius'] = fifty_pct_radius
    results['pct90_radius'] = ninety_pct_radius
    return results

# Given one user's tweets, returns a Counter of neighborhood name -> number of
# times they tweeted in that neighborhood.
def get_user_nghds(tweets):
    user_nghds = collections.Counter()
    for tweet in tweets:
        # print [n.properties['HOOD'] for n in nghds[0:5]]
        user_nghd_name = get_neighborhood_name(nghds,
            tweet['coordinates'][0],
            tweet['coordinates'][1])
        user_nghds[user_nghd_name] += 1
    
    return user_nghds

# Given a python object representing one twitter user, returns a string of SQL
# you can run to enter them into the DB.
def user_to_input_string(user):
    lat = user['centroid'][1]
    lon = user['centroid'][0]
    centroid = ppygis.Point(lon, lat, srid=4326)
    neighborhoods = make_hstore(user['neighborhoods'])
    
    insert_str = pg_cur.mogrify("INSERT INTO user_pgh(screen_name, " +
            "num_tweets, most_common_neighborhood, neighborhoods, " +
            "pct50_radius, pct90_radius, centroid) VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (user['screen_name'],
             user['num_tweets'], user['most_common_neighborhood'], neighborhoods,
             user['pct50_radius'], user['pct90_radius'], centroid))
    return insert_str

 
def doAll():
    # Create the table. Delete if it already existed.
    print "About to dump and recreate Postgres user_pgh table. Enter to continue, Ctrl-C to quit."
    raw_input()
    pg_cur.execute("DROP TABLE IF EXISTS user_pgh;")
    psql_conn.commit()
    create_table_str = "CREATE TABLE user_pgh(id SERIAL PRIMARY KEY, " +\
        "screen_name text, num_tweets integer, most_common_neighborhood text, " +\
        "neighborhoods hstore, pct50_radius real, pct90_radius real);"
    pg_cur.execute(create_table_str)
    psql_conn.commit()
    pg_cur.execute("SELECT AddGeometryColumn('user_pgh', 'centroid', 4326, 'POINT', 2);")
    psql_conn.commit()

    print "loading neighborhoods"
    global nghds # TODO ugh
    nghds = load_nghds()
    print "done"

    # Get all the user IDs that have ever tweeted.
    print "Getting user ids"
    user_screen_names = set()
    counter = 0
    pg_cur.execute("SELECT user_screen_name FROM tweet_pgh;")
    for row in pg_cur:
        user_screen_names.add(row[0])
        counter += 1
        if counter % 1000 == 0:
            print 'Tweets processed: ' + str(counter)

    print "Got user ids. This many: " + str(len(user_screen_names))


    # For each one, enter them into the user table.
    for user_screen_name in user_screen_names:
        user = {}

        try:
            tweets = []
            pg_cur.execute("SELECT ST_AsGeoJSON(coordinates) FROM tweet_pgh WHERE user_screen_name=%s;", (user_screen_name,))
            for row in pg_cur:
                tweets.append({'coordinates': json.loads(row[0])['coordinates']})

            user['screen_name'] = user_screen_name
            user['num_tweets'] = len(tweets)

            centroid_radii = generate_centroids_and_radii(tweets)
            user.update(centroid_radii)

            user_nghds = get_user_nghds(tweets)
            user['neighborhoods'] = dict(user_nghds)
            if len(user_nghds) > 0:
                user['most_common_neighborhood'] = user_nghds.most_common(1)[0][0]
            else:
                user['most_common_neighborhood'] = 'Outside Pittsburgh'
                print 'Huh? User has zero tweets in neighborhoods?' + user_screen_name
            # print user
            pg_cur.execute(user_to_input_string(user))
            psql_conn.commit()
        
        except Exception as e:
            print 'Exception: ' + str(e)
    psql_conn.commit()

if __name__ == '__main__':
    cProfile.run("doAll()")    
