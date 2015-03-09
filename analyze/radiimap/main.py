#!/usr/bin/env python

import os
import sys
import pymongo
import random
from flask import Flask, render_template, request, jsonify, json, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
sys.path.append('../user/')
import build_user_collection as NGHD
from build_user_coll_sde import generate_centroids_and_sd
import cProfile, pstats, StringIO
from csv import DictWriter, DictReader

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
bin_to_nghds = {}

def load_nghds(module):
    print 'loading neighborhoods...'
    for line in DictReader(open(module)):
        bin_to_nghds[(float(line['lat']), float(line['lon']))] = line['nghd']
    print 'done loading neighborhoods!'
    return

# from https://github.com/dantasse/nghd_info/blob/master/util/util.py
# Rounds lat and lon to 2 decimal places and returns a tuple of them both.
def round_latlon(lat, lon):
    if lat is None or lon is None:
        return (None, None)
    return (round(float(lat), 2), round(float(lon), 2))

def random_sample(col, query, num):
    cursor = db[col].find(query)
    total = cursor.count()
    print "col:" + str(total)
    result = []
    indices = set()
    while len(result) < num:
        random_num = random.randint(0, total)
        while random_num in indices:
            random_num = random.randint(0, total)
        indices.add(random_num)
        record = cursor[random_num]
        result.append(record)
    return result

# This call kicks off all the main page rendering.
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/get-all-tweets', methods=['GET'])
def get_all_tweets():
    cursor = db['tweet_pgh'].find({'$query': {}, '$maxTimeMS': 10000}).limit(10000)
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

    tweets = to_serializable_list(get_tweets_from_user(user_screen_name))
    return jsonify(tweets=tweets)

# Returns given user's tweet range.
@app.route('/get-user-tweet-range', methods=['GET'])
def get_user_tweet_range():
    user_screen_name = request.args.get('user_screen_name', '', type=str)
    if user_screen_name == '':
        return jsonify([])

    cursor = db['user_SDE'].find_one({'screen_name': user_screen_name})
    cursor = to_serializable(cursor)
    print cursor
    return jsonify(tweet_range=cursor)

@app.route('/get-ngbh-tweets', methods=['GET'])
def get_ngbh_tweets():
    pr = cProfile.Profile()
    pr.enable()
    # ---------------- start profiling the whole thing ----------------

    neighborhood = request.args.get('neighborhood', '', type=str)
    if neighborhood == '':
        return jsonify([])
    num_users = request.args.get('user_num', 10, type=int)
    num_tweets_per_user = request.args.get('num_tweets_per_user', 10, type=int)
    randomize = request.args.get('randomize', 'false', type=str)
    if randomize == 'false': randomize = False
    else: randomize = True

    print 'randomized? ' + str(randomize) + ', num users: ' + str(num_users) + ', num tweets per user: ' + str(num_tweets_per_user)
    if randomize:
        users = random_sample('user', {'most_common_neighborhood': neighborhood}, num_users)
    else:
        users = db['user'].find({'most_common_neighborhood': neighborhood}).limit(num_users)
    tweets = []

    if not bin_to_nghds:
        load_nghds('point_map.csv')

    for user in users:
         tmp = db['tweet_pgh'].find({'user.screen_name': user['screen_name']}).limit(num_tweets_per_user)
         for t in tmp:
             bin_coord = round_latlon(t["geo"]["coordinates"][0], t["geo"]["coordinates"][1])
             if bin_coord in bin_to_nghds:
                 nghd = bin_to_nghds[bin_coord]
             else:
                 nghd = 'Outside Pittsburgh'
             t["neighborhood"] = nghd
             tweets.append(t)

    # ---------------- end profiling the whole thing ----------------

    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby)
    ps.print_stats(10)
    print s.getvalue()

    return jsonify(tweets=to_serializable_list(tweets))

@app.route('/get-ngbh-range', methods=['GET'])
def get_ngbh_range():
    neighborhood = request.args.get('neighborhood', '', type=str)
    if neighborhood == '':
        return jsonify([])

    users = db['user'].find({'most_common_neighborhood': neighborhood}).limit(100)
    #print len(users)
    tweets = []
    for user in users:
         tweets += db['tweet_pgh'].find({'user.screen_name': user['screen_name']})
    result = generate_centroids_and_sd(tweets)
    return jsonify(result=result)

# Returns list of tweet ranges of 10 users who tweet the most
@app.route('/get-top-10-user-tweet-range', methods=['GET'])
def get_top_10_user_tweet_range():
    cursor = db['user'].find().sort("num_tweets", -1).limit(10)
    for v in range(0,3):
        print cursor[v]
    return jsonify(tweet_ranges=to_serializable_list(cursor))

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

def to_serializable(mongodb_cursor):
    if mongodb_cursor:
        del mongodb_cursor['_id']
    return mongodb_cursor

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
    app.run(host='0.0.0.0', port=1025)  # listen on all public IPs
