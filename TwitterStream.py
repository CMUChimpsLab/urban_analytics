#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Gustav Arngården

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# From https://github.com/arngarden/TwitterStream/blob/master/TwitterStream.py

import sys
import inspect
import time
import pycurl
import urllib
import json
import oauth2 as oauth
from pymongo import Connection

db = Connection('localhost',27017)['tweet']

API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
#USER_AGENT = 'TwitterStream 1.0' # This can be anything really

# You need to replace these with your own values
OAUTH_KEYS = {'consumer_key': '',
              'consumer_secret': '',
              'access_token_key': '',
              'access_token_secret': ''}

# These values are posted when setting up the connection
POST_PARAMS = {#'include_entities': 0,
               #'stall_warning': 'true',
               #'track': 'iphone,ipad,ipod'}
               #'locations': '-122.5950,37.565,-122.295,37.865'}# San Francisco
                'locations': '-80.2,40.241667,-79.8,40.641667'}# Pgh
# Locations are lower left long, lower left lat, upper right long, upper right lat
# This is a pretty arbitrarily chosen square roughly around Pittsburgh.
# Center of Pittsburgh is 40.441667, -80.0 (exactly -80) so I went .2 deg long
# and .2 deg lat. Captures most of Pittsburgh and suburbs.
#
# More info: https://dev.twitter.com/docs/streaming-apis/parameters#locations
# Can use -180,-90,180,90 to get all geotagged tweets.

def getLineNo():
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  #pass#print info.filename                       # __FILE__     -> Test.py
  #pass#print info.function                       # __FUNCTION__ -> Main
  return ' line:' + str(info.lineno)

class TwitterStream:
    def __init__(self, timeout=False):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        # self.setup_connection()

    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        # self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

        self.conn.setopt(pycurl.VERBOSE, True)

    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_URL,
                                                                             urllib.urlencode(POST_PARAMS)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def start(self):
        """ Start listening to Streaming endpoint.
        Handle exceptions according to Twitter's recommendations.
        """
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True:
            self.setup_connection() # I guess make sure the connection is open?
            try:
                self.conn.perform()
            except Exception as e:
                # print '%d'%(time.time()) +getLineNo() + ':', e
                # Network error, use linear back off up to 16 seconds
                print '%d'%(time.time()) +getLineNo() + ':', 'Network error: %s' % self.conn.errstr()
                print '%d'%(time.time()) +getLineNo() + ':', 'Waiting %s seconds before trying again' % backoff_network_error
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                print '%d'%(time.time()) +getLineNo() + ':', 'Rate limit, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                print '%d'%(time.time()) +getLineNo() + ':', 'HTTP error %s, %s' % (sc, self.conn.errstr())
                print '%d'%(time.time()) +getLineNo() + ':', 'Waiting %s seconds' % backoff_http_error
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            msg = ''
            if message.get('limit'):
                print '%d'%(time.time()) +getLineNo() + ':', 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                print '%d'%(time.time()) +getLineNo() + ':', 'Got warning: %s' % message['warning'].get('message')
            else:
                db.tweet_pgh.insert(dict(message))
                print '%d'%(time.time()) +getLineNo() + ':', 'Got tweet with text: %s' % message.get('text').encode('utf-8')
        sys.stdout.flush()
        sys.stderr.flush()
        return len(data)
        


if __name__ == '__main__':
    timestamp = time.time()
    errFile = open('twitter_error_%d.log'%(timestamp), 'w')
    outFile = open('twitter_output_%d.log'%(timestamp), 'w')
    sys.stdout = outFile
    sys.stderr = errFile
    ts = TwitterStream()
    ts.setup_connection()
    ts.start()
