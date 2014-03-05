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
    result1 = cursor.next()
    del result1['_id'] # because it's an ObjectId; not serializable to json

    return flask.json.jsonify(result1)

if __name__ == "__main__":
    app.run(debug=True) # TODO remove this from anything deployed

