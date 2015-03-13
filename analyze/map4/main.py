#!/usr/bin/env python

import os, json, csv, psycopg2, psycopg2.extensions, psycopg2.extras
from osgeo import ogr
from collections import Counter
from flask import Flask, render_template, request, jsonify, json, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
ogr.UseExceptions()

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
            'user': {'screen_name': user_screen_name},
            'text': row['text']})

    return results

# Returns tweets from a given user.
@app.route('/get-user-tweets', methods=['GET'])
def get_user_tweets():
    user_screen_name = request.args.get('user_screen_name', '', type=str)
    if user_screen_name == '':
        return jsonify([])

    tweets = get_tweets_from_user(user_screen_name)
    return jsonify(tweets=tweets)

def get_tweets_from_user(user_screen_name):
    pg_cur.execute('SELECT ST_AsGeoJSON(coordinates) AS coords, text FROM tweet_pgh WHERE user_screen_name=%s;', (user_screen_name,))
    results = []
    for row in pg_cur.fetchall():
        results.append({'coordinates': json.loads(row['coords']),
            'user': {'screen_name': user_screen_name},
            'text': row['text']})
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0')
