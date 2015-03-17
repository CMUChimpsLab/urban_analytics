#!/usr/bin/env python

import os, json, csv, psycopg2, psycopg2.extensions, psycopg2.extras
from collections import Counter
from flask import Flask, render_template, request, jsonify, json, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# general flask app settings
app = Flask(__name__)
app.secret_key = 'some_secret'
app.debug = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
toolbar = DebugToolbarExtension(app)
users = {} # ugh global. screen names in here are lowercase.

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
psql_conn = psycopg2.connect("dbname='tweet'")
pg_cur = psql_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# This call kicks off all the main page rendering.
@app.route('/')
def index():
    return render_template('main.html')

# not actually "all" tweets, but 20k of them.
@app.route('/get-all-tweets', methods=['GET'])
def get_all_tweets():
    pg_cur.execute('SELECT ST_AsGeoJSON(coordinates) AS coords, text FROM tweet_pgh LIMIT 20000;')
    results = []
    for row in pg_cur.fetchall():
        results.append({'coordinates': json.loads(row['coords']),
            'user': {'screen_name': row['user_screen_name']},
            'text': row['text']})

    return results

# Returns tweets from a given user.
@app.route('/get-user-tweets', methods=['GET'])
def get_user_tweets():
    user_screen_name = request.args.get('user_screen_name', '', type=str)
    if user_screen_name == '':
        return jsonify([])

    print "starting to call stuff from postgres"
    tweets = get_tweets_from_users(user_screen_name)
    print "done calling postgres"
    return jsonify(tweets=tweets)

# Returns tweets from all users who have ever tweeted in this area.
@app.route('/get-user-tweets-from-area', methods=['GET'])
def get_user_tweets_from_area():
    tweets_from_area = get_tweets_from_area(request)
    users_in_area = tuple(set([t['user']['screen_name'] for t in tweets_from_area]))
    print 'This many users: ' + str(len(users_in_area))
    tweets_from_users = get_tweets_from_users(users_in_area)
    print 'This many tweets: ' + str(len(tweets_from_users))
    tweets_per_user = create_tweets_per_user_map(tweets_from_users)
    return jsonify(users=tweets_per_user)

# give it a list of tweets, it returns a map of user_screen_name -> tweets
def create_tweets_per_user_map(all_tweets):
    tweets_per_user = {}
    for tweet in all_tweets:
        user_screen_name = tweet['user']['screen_name']
        # TODO change to defaultdict(list)
        if not user_screen_name in tweets_per_user.keys():
            tweets_per_user[user_screen_name] = [tweet]
        else:
            tweets_per_user[user_screen_name].append(tweet)
    return tweets_per_user

def get_tweets_from_area(req):
    ne_lat = req.args.get('ne_lat', 0, type=float)
    ne_lng = req.args.get('ne_lng', 0, type=float)
    sw_lat = req.args.get('sw_lat', 0, type=float)
    sw_lng = req.args.get('sw_lng', 0, type=float)

    pg_cur.execute('SELECT ST_AsGeoJSON(coordinates) AS coords, user_screen_name, text' +        ' FROM tweet_pgh WHERE ST_MakeEnvelope(%s, %s, %s, %s) ~ coordinates;',
        (sw_lng, sw_lat, ne_lng, ne_lat))
    results = []
    for row in pg_cur.fetchall():
        results.append({'coordinates': json.loads(row['coords']),
            'user': {'screen_name': row['user_screen_name']},
            'text': row['text']})
    return results

def get_tweets_from_users(user_screen_names):
    if type(user_screen_names) == type('asdf'):
        user_screen_names = [user_screen_names] # hack so you can pass a single
        # value if you want.

    pg_cur.execute('SELECT ST_AsGeoJSON(coordinates) AS coords, text, user_screen_name' +
        ' FROM tweet_pgh WHERE user_screen_name IN %s;', (user_screen_names,))
    results = []
    for row in pg_cur.fetchall():
        results.append({'coordinates': json.loads(row['coords']),
            'user': {'screen_name': row['user_screen_name']},
            'text': row['text']})
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0')
