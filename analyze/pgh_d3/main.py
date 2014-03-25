#!/usr/bin/env python

# Server side for plotting things around Pittsburgh.

import flask, pymongo, json, urllib

app = flask.Flask(__name__)
dbclient = pymongo.MongoClient('localhost', 27017)
# or: dbclient = pymongo.MongoClient('mongodb://localhost:27017')
db = dbclient['tweet']

@app.route('/')
def main():
    return flask.render_template('index.html')

@app.route('/query')
def query():
    # request.args.keys()[0] is a string representing the whole query
    cursor = db.tweet_pgh.find(json.loads(flask.request.args.keys()[0]))
    cursor.limit(2000) # TODO update this limit based on user input
    results = list(cursor)

    for result in results:
        del result['_id'] # because it's an ObjectId; not serializable to json

    # got to make this a dict, not array, "for security reasons", whatever that means
    return flask.json.jsonify({'results': results})

@app.route('/user_centroid_query')
def user_centroid_query():
    args = flask.request.args
    tl_lon = float(args['top_left_lon'])
    tl_lat = float(args['top_left_lat'])
    br_lon = float(args['bottom_right_lon'])
    br_lat = float(args['bottom_right_lat'])
    cursor = db.user.find()
    tweets_to_return = []

    for user in cursor:
        user_lon = float(user['centroid'][0])
        user_lat = float(user['centroid'][1])
        if user_lon > tl_lon and user_lon < br_lon and\
            user_lat > br_lat and user_lat < tl_lat:
            that_users_tweets = db.tweet_pgh.find({'user.id': user['_id']})
            for tweet in that_users_tweets:
                del tweet['_id'] # b/c it's not serializable
                tweets_to_return.append(tweet)
        
    return flask.json.jsonify({'results':tweets_to_return})

if __name__ == "__main__":
    app.run(debug=True) # TODO remove this from anything deployed

