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
    return flask.json.jsonify({'results':"hello world"})

if __name__ == "__main__":
    app.run(debug=True) # TODO remove this from anything deployed

