#!/usr/bin/env python

# Server side for plotting things around Pittsburgh.

import flask, pymongo, json, urllib
from flask import request

app = flask.Flask(__name__)
dbclient = pymongo.MongoClient('localhost', 27017)
# or: dbclient = pymongo.MongoClient('mongodb://localhost:27017')
db = dbclient['tweet']

@app.route('/')
def main():
    return flask.render_template('index.html')

@app.route('/query')
def query():
    urlquery = request.args.get('query', '')
    querydecoded = urllib.unquote(urlquery).decode('utf8')
    queryjson = json.loads(querydecoded)
    print queryjson

    cursor = db.tweet_pgh.find(queryjson)
    result1 = cursor.next()
    return result1

if __name__ == "__main__":
    app.run()

