#!/usr/bin/env python

import os
import pymongo
from flask import Flask, render_template, request, jsonify, json, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# general flask app settings
app = Flask(__name__)
app.secret_key = 'some_secret'
# related to debugging
app.debug = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
toolbar = DebugToolbarExtension(app)
# related to db
db_client = pymongo.MongoClient('localhost', 27017)
db = db_client['tweet']


# This call kicks off all the main page rendering.
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/get-all-tweets', methods=['GET'])
def get_all_tweets():
    cursor = db['tweet_pgh'].find({'$query': {}, '$maxTimeMS': 10000}).limit(2000)
    return jsonify(tweets=to_serializable_list(cursor))

@app.route('/get-all-tweets-from-area', methods=['GET'])
def get_all_tweets_from_area():
    return jsonify(tweets=to_serializable_list(get_tweets_from_area(request)))

# Returns tweets from a given user.
@app.route('/get-user-tweets', methods=['GET'])
def get_user_tweets():
    user_screen_name = request.args.get('user_screen_name', '', type=str)
    if user_screen_name == '':
        return jsonify([])

    return jsonify(tweets=to_serializable_list(get_tweets_from_user(user_screen_name)))


# Returns tweets from people who have tweeted in that area.
@app.route('/get-user-tweets-from-area', methods=['GET'])
def get_user_tweets_from_area():
    users = {}
    tweets_from_area = get_tweets_from_area(request)

    for tweet in tweets_from_area:
        user_screen_name = tweet['user']['screen_name']
        if not user_screen_name in users.keys():
            users[user_screen_name] = to_serializable_list(get_tweets_from_user(user_screen_name))

    return jsonify(users=users)


# Given a cursor, returns a list of all the items in that cursor. So if you
# have a ton of things in this list, it may be not so effective.
def to_serializable_list(mongodb_cursor):
    data = list(mongodb_cursor)
    for d in data:
        del d['_id']  # because it's an ObjectId; not serializable to json (reference from Dan)
    return data


def get_tweets_from_user(user_screen_name):
    cursor = db['tweet_pgh'].find({'$query': {'user.screen_name': user_screen_name},
                                        # '$orderBy': 'created_at',
                                        '$maxTimeMS': 10000}).limit(2000)
    # data = db['tweet_pgh'].find({'$query': {'user.screen_name': {'$in': tweets_by_users}},
    #                                   '$maxTimeMS': 10000}).limit(2000)
    return cursor


def get_tweets_from_area(req):
    ne_lat = req.args.get('ne_lat', 0, type=float)
    ne_lng = req.args.get('ne_lng', 0, type=float)
    sw_lat = req.args.get('sw_lat', 0, type=float)
    sw_lng = req.args.get('sw_lng', 0, type=float)
    cursor = db['tweet_pgh'].find({'$query': {'$and': [{'geo.coordinates.0': {'$gt': sw_lat, '$lt': ne_lat}},
                                                            {'geo.coordinates.1': {'$gt': sw_lng, '$lt': ne_lng}}]},
                                        '$maxTimeMS': 10000}).limit(2000)

    return cursor


if __name__ == '__main__':
    db['tweet_pgh'].ensure_index('_id')
    db['tweet_pgh'].ensure_index('geo.coordinates.0')
    db['tweet_pgh'].ensure_index('geo.coordinates.1')
    db['tweet_pgh'].ensure_index('user.screen_name')
    app.run(host='0.0.0.0')  # listen on all public IPs
