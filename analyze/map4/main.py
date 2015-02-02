#!/usr/bin/env python

import os, pymongo, json, csv
from collections import Counter
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
users = {} # ugh global. screen names in here are lowercase.

# Creates a dict of user: {bunch of info including tweets:[...]}
def init_tweets_and_responses():
    survey_responses = csv.reader(open('../home_work/twitter_home_work_clean.csv', 'rU'))
    # tweets = json.load(open('../home_work/tweets.json'))
    survey_responses.next()
    for row in survey_responses:
        screen_name = row[1].lower()
        try:
            users[screen_name] = {'home_lat': float(row[6]), 'home_lon': float(row[7])}
        except ValueError as ve:
            continue

# This call kicks off all the main page rendering.
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/get-all-tweets', methods=['GET'])
def get_all_tweets():
    cursor = db['tweet_pgh'].find({'$query': {}, '$maxTimeMS': 100000}).limit(2000)
    tweets=to_serializable_list(cursor)
    for tweet in tweets:
        tweet['coordinates']['coordinates'] = round_latlon(tweet['coordinates']['coordinates'])
    return jsonify(tweets=tweets)

# Rounds a tweet's coordinates to the nearest .001 for lat and long. Takes a
# tuple as input, returns a tuple as output.
def round_latlon(pair):
    return (round(pair[0], 3), round(pair[1], 3))
 
# Returns a tuple of the prediction where the person most likely lives.
def make_prediction(tweets):
    rounded_tweets = [round_latlon(tweet['coordinates']['coordinates']) for tweet in tweets]
    counter = Counter(rounded_tweets)
    return counter.most_common(1)[0][0]

# Returns tweets from a given user.
@app.route('/get-user-tweets', methods=['GET'])
def get_user_tweets():
    user_screen_name = request.args.get('user_screen_name', '', type=str)
    if user_screen_name == '':
        return jsonify([])

    tweets=to_serializable_list(get_tweets_from_user(user_screen_name))
    for tweet in tweets:
        tweet['coordinates']['coordinates'] = round_latlon(tweet['coordinates']['coordinates'])
        print tweet['text']

    user_survey = users[user_screen_name.lower()]
    home_location = round_latlon((user_survey['home_lat'], user_survey['home_lon']))
    prediction = make_prediction(tweets)

    return jsonify(tweets=tweets, user_home=home_location, prediction=prediction)

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
                                        '$maxTimeMS': 100000}).limit(2000)
    return cursor

if __name__ == '__main__':
    print 'ensuring indexes...'
    db['tweet_pgh'].ensure_index('_id')
    db['tweet_pgh'].ensure_index('coordinates.coordinates.0')
    db['tweet_pgh'].ensure_index('coordinates.coordinates.1')
    db['tweet_pgh'].ensure_index('user.screen_name')
    init_tweets_and_responses()
    print 'indexes done, starting server'
    app.run(host='0.0.0.0')
