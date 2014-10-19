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

def load_nghds():
    neighborhoods = geojson.load(open('static/neighborhoods.json'))
    nghd_features = neighborhoods['features']
    for nghd in nghd_features:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    return nghd_features

# return all users who tweet mostly in a given neighborhood
@app.route('/nghd_users')
def nghd_users():
    nghd_name = flask.request.args['nghd']
    users = db['user'].find({'most_common_neighborhood': nghd_name})
    return flask.json.jsonify({'results': list(users)})


if __name__ == "__main__":
    print "ensuring indexes"
    db['user'].ensure_index('_id')
    db['user'].ensure_index('most_common_neighborhood')
    db['user'].ensure_index([('centroid', pymongo.GEOSPHERE)])
    db['tweet_pgh_good'].ensure_index([('coordinates', pymongo.GEOSPHERE)])
    db['foursquare'].ensure_index([('coordinates', pymongo.GEOSPHERE)])
    print "indexes have all been created, starting app"
    nghds = load_nghds()
    app.run(host='0.0.0.0', debug=True)
    # 0.0.0.0 means "listen on all public IPs"

