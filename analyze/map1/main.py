#!/usr/bin/env python

# We're going to find out where else people in each neighborhood go.
# People who most commonly tweet in that neighborhood: where are the rest of
# their tweets?

import flask, pymongo, json, urllib, random, datetime, shapely.geometry, geojson

app = flask.Flask(__name__)
dbclient = pymongo.MongoClient('localhost', 27017)
# or: dbclient = pymongo.MongoClient('mongodb://localhost:27017')
db = dbclient['tweet']
nghds = []

@app.route('/')
def main():
    return flask.render_template('index.html')

@app.route('/bunch_of_tweets')
def get_a_bunch_of_tweets():
    limit = int(flask.request.args['limit'])
    cursor = db['tweet_pgh'].find().limit(limit)
    good_keys = ['text', 'id', 'user', 'coordinates', 'created_at']
    good_user_keys = ['id', 'screen_name']
    
    tweets_to_return = []
    for tweet in cursor:
        small_tweet = dict([(key, tweet[key]) for key in good_keys])
        small_tweet['user'] = dict([(key, tweet['user'][key]) for key in good_user_keys])
        tweets_to_return.append(small_tweet)

    # has to be a dict, not array, "for security reasons", whatever that means
    return flask.json.jsonify({'results': tweets_to_return})

def load_nghds():
    neighborhoods = geojson.load(open('static/neighborhoods.json'))
    nghd_features = neighborhoods['features']
    for nghd in nghd_features:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    return nghd_features

def get_neighborhood_name(nghds, lon, lat):
    point = shapely.geometry.Point(lon, lat)
    for nghd in nghds:
        if nghd['shape'].contains(point):
            return nghd.properties['HOOD']
    return 'Outside Pittsburgh'

# Returns tweets by people who most commonly tweet in the neighborhood that
# you clicked in.
@app.route('/tweets_by_this_nghd_users')
def get_tweets_by_this_nghd_users():
    limit = int(flask.request.args['limit'])
    lon = float(flask.request.args['lon'])
    lat = float(flask.request.args['lat'])
    good_keys = ['text', 'id', 'user', 'coordinates', 'created_at']
    good_user_keys = ['id', 'screen_name']
    nghd_name = get_neighborhood_name(nghds, lon, lat)

    users = db['user'].find({'most_common_neighborhood': nghd_name})
    tweets_to_return = []
    for user in users:
        tweets = db['tweet_pgh'].find({'user.id': user['_id']})
        for tweet in tweets:
            small_tweet = dict([(key, tweet[key]) for key in good_keys])
            small_tweet['user'] = dict([(key, tweet['user'][key]) for key in good_user_keys])
            tweets_to_return.append(small_tweet)
    return flask.json.jsonify({'results': tweets_to_return})


    

if __name__ == "__main__":
    print "ensuring indexes"
    db['user'].ensure_index('_id')
    db['user'].ensure_index('most_common_neighborhood')
    # db['user'].ensure_index([('centroid', pymongo.GEOSPHERE)])
    # db['tweet_pgh'].ensure_index([('coordinates', pymongo.GEOSPHERE)])
    # db['foursquare'].ensure_index([('coordinates', pymongo.GEOSPHERE)])
    print "indexes have all been created, starting app"
    nghds = load_nghds()
    app.run(host='0.0.0.0')
    # 0.0.0.0 means "listen on all public IPs"

