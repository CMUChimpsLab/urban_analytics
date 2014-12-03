#!/usr/bin/env python

# Just output the correct capitalization for everyone who's not capitalized right.

import csv, urllib, ConfigParser, time, json
import oauth2 as oauth

config = ConfigParser.ConfigParser()
config.read('config.txt')

# details for Users/show query: https://dev.twitter.com/rest/reference/get/users/show
TWITTER_URL = 'https://api.twitter.com/1.1/users/show.json'
OAUTH_KEYS = {'consumer_key': config.get('twitter', 'consumer_key'),
              'consumer_secret': config.get('twitter', 'consumer_secret'),
              'access_token_key': config.get('twitter', 'access_token_key'),
              'access_token_secret': config.get('twitter', 'access_token_secret')}

def oauth_req(url, http_method="GET", post_body=None, http_headers=None):
    consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
    token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
    client = oauth.Client(consumer, token)
    resp, content = client.request(url, method=http_method, headers=http_headers)
    return (resp, content)

counter = 2 # yep. for easy indexing into excel w/ a header row.
reader = csv.reader(open('twitter_home_work_clean.csv', 'rU'))
reader.next() #ignore header row

for line in reader:
    entered_name = line[1]
    print entered_name
    params = {'screen_name': line[1]}
    (resp, content) = oauth_req(TWITTER_URL + '?' + urllib.urlencode(params), 'GET')
    real_name = json.loads(content)['screen_name']
    if real_name != entered_name:
        print '    *** user %03d real name: %s' % (counter, real_name)
    counter += 1
    time.sleep(5)
