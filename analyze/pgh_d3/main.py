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
    cursor = db.tweet_pgh_good.find(json.loads(flask.request.args.keys()[0]))
    cursor.limit(2000) # TODO update this limit based on user input
    results = list(cursor)

    for result in results:
        del result['_id'] # because it's an ObjectId; not serializable to json

    # has to be a dict, not array, "for security reasons", whatever that means
    return flask.json.jsonify({'results': results})

@app.route('/user_centroid_query')
def user_centroid_query():
    args = flask.request.args
    tl_lon = float(args['top_left_lon'])
    tl_lat = float(args['top_left_lat'])
    br_lon = float(args['bottom_right_lon'])
    br_lat = float(args['bottom_right_lat'])
    if args['limit']:
        limit = int(args['limit'])
    else:
        limit = 0
    tweets_to_return = []

    search_rect = {'type': 'Polygon', 'coordinates': [[
        [tl_lon, tl_lat],
        [tl_lon, br_lat],
        [br_lon, br_lat],
        [br_lon, tl_lat],
        [tl_lon, tl_lat]]]}
    # Note this is a list of lists of coordinates. (you might have multiple
    # lists of coordinates; like if you have inner rings like a donut.)
    # Note also that the first and last coordinate are the same.

    cursor = db['user'].find(
        {'centroid':
            {'$geoWithin':
                {'$geometry': search_rect}
            }
        })
    for user in cursor:
        that_users_tweets = db['tweet_pgh_good'].find({'user.id': user['_id']})
        for tweet in that_users_tweets:
            del tweet['_id'] # b/c it's not serializable
            tweets_to_return.append(tweet)
        if limit and len(tweets_to_return) >= limit:
            break
        
    return flask.json.jsonify({'results':tweets_to_return})

@app.route('/user_here_once_query')
def user_here_once_query():
    print "user here once"
    args = flask.request.args
    tl_lon = float(args['top_left_lon'])
    tl_lat = float(args['top_left_lat'])
    br_lon = float(args['bottom_right_lon'])
    br_lat = float(args['bottom_right_lat'])
    if args['limit']:
        limit = int(args['limit'])
    else:
        limit = 0
    
    tweets_to_return = []
    search_rect = {'type': 'Polygon', 'coordinates': [[
        [tl_lon, tl_lat],
        [tl_lon, br_lat],
        [br_lon, br_lat],
        [br_lon, tl_lat],
        [tl_lon, tl_lat]]]}
    tweets_in_rect = db['tweet_pgh_good'].find(
        {'coordinates':
            {'$geoWithin':
                {'$geometry': search_rect}
            }
        })
    for tweet_in_rect in tweets_in_rect:
        that_users_tweets = db['tweet_pgh_good'].find({
            'user.id': tweet_in_rect['user']['id']
        })
        for tweet in that_users_tweets:
            del tweet['_id'] # not serializable
            tweets_to_return.append(tweet)
        if limit and len(tweets_to_return) >= limit:
            break

    return flask.json.jsonify({'results':tweets_to_return})


if __name__ == "__main__":
    print "ensuring indexes"
    db['user'].ensure_index('_id')
    db['user'].ensure_index([('centroid', pymongo.GEOSPHERE)])
    db['tweet_pgh_good'].ensure_index([('coordinates', pymongo.GEOSPHERE)])
    print "indexes have all been created, starting app"
    app.run(host='0.0.0.0')
    # 0.0.0.0 means "listen on all public IPs"

