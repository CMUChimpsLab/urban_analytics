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

import sys, argparse, inspect, time, pycurl, urllib, json, ConfigParser
import requests, HTMLParser, traceback
import oauth2 as oauth
import load_tweets_into_postgres, psycopg2, psycopg2.extensions, psycopg2.extras

API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'

config = ConfigParser.ConfigParser()
config.read('config.txt')

NUM_TWITTER_CREDENTIALS = int(config.get('num_twitter_credentials', 'num'))
MIN_NUM_RECONNECT = 1
FOURSQUARE_API_VERSION = '20140806'

CITY_LOCATIONS = {
    'pgh':  { 'locations': '-80.2,40.241667,-79.8,40.641667' },
    'sf':   { 'locations': '-122.5950,37.565,-122.295,37.865' },
    'ny':   { 'locations': '-74.03095193,40.6815699768,-73.9130315074,40.8343765254' },
    'houston': { 'locations': '-95.592778, 29.550556, -95.138056, 29.958333' },
    'detroit': { 'locations': '-83.2458, 42.1314, -82.8458, 42.5314' },
    'chicago': { 'locations': '-87.9847, 41.6369, -87.5847, 42.0369' },
    'cleveland': { 'locations': '-81.9697, 41.1822, -81.4697, 41.5822' },
    'seattle': { 'locations': '-122.5331, 47.4097, -121.9331, 47.8097' },
    'miami': { 'locations': '-80.4241, 25.5877, -80.0641, 26.2877' },
    'london': { 'locations': '-0.4275, 51.3072, 0.2525, 51.7072' },
    'minneapolis': { 'locations': '-93.465, 44.7778, -93.065, 45.1778' }
}
# Locations are lower left long, lower left lat, upper right long, upper right lat.
# Mostly pretty arbitrarily chosen.
#
# Note! If there is a |coordinates| field in the tweet, that will be tested
# against our parameters here. If not, the |place.bounding_box| will be tested,
# and ANY overlap will match. This means we'll get a ton of tweets that are
# not in Pittsburgh, just because they're very inaccuate and so have a huge
# bounding box.
#
# More info: https://dev.twitter.com/docs/streaming-apis/parameters#locations
# Can use -180,-90,180,90 to get all geotagged tweets.

#  CITY_COLLECTIONS: city -> tweet_collection * foursquare_collection
CITY_COLLECTIONS = {
    'pgh':  ('tweet_pgh', 'foursquare_pgh'),
    'sf':   ('tweet_sf', 'foursquare_sf'),
    'ny':   ('tweet_ny', 'foursquare_ny'),
    'houston': ('tweet_houston','foursquare_houston'),
    'detroit': ('tweet_detroit','foursquare_detroit'),
    'chicago': ('tweet_chicago','foursquare_chicago'),
    'cleveland':('tweet_cleveland','foursquare_cleveland'),
    'seattle': ('tweet_seattle','foursquare_seattle'),
    'miami': ('tweet_miami','foursquare_miami'),
    'london': ('tweet_london','foursquare_london'),
    'minneapolis': ('tweet_minneapolis','foursquare_minneapolis')
}

   
# Prints out a log including the stack trace, time, and a message, when an
# exception has occurred.
def log_exception(message):
    traceback.print_exc()

# Prints out a log including the time and a message.
def log(message):
    callerframerecord = inspect.stack()[1] # 0=this line, 1=line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    line_no = int(info.lineno)
    print '%d, line %d: %s' % (time.time(), line_no, message)


 
class TwitterStream:
    def __init__(self, city, timeout=False):
        self.credential_num = 1
        self.set_credentials()

        self.conn = None
        self.html_parser = HTMLParser.HTMLParser()
        self.buffer = ''
        self.timeout = timeout
        if not (city in CITY_LOCATIONS and city in CITY_COLLECTIONS):
            raise Exception("city not valid")
        self.city = city
        self.post_params = CITY_LOCATIONS.get(self.city)
        coords = CITY_LOCATIONS[self.city]['locations'].split(',')
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = map(float, coords)
        self.tweet_col, self.foursquare_col = CITY_COLLECTIONS.get(self.city)
        self.num_reconnect = 0
        self.setup_connection()

        # set up the Postgres connection.
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        self.psql_conn = psycopg2.connect("dbname='tweet'")
        psycopg2.extras.register_hstore(self.psql_conn)
        self.pg_cur = self.psql_conn.cursor()

    # Given a tweet from the Twitter API, saves it to Postgres DB table |table|.
    def save_to_postgres(self, tweet):
        insert_str = load_tweets_into_postgres.tweet_to_insert_string(tweet, self.tweet_col)
        try:
            self.pg_cur.execute(insert_str)
            self.psql_conn.commit()
        except Exception as e:
            print "Error running this command: %s" % insert_str
            traceback.print_exc()
            traceback.print_stack()

    def set_credentials(self):
        log('setting api credentials num %s' % self.credential_num)
        twitter_cred_name = 'twitter-' + str(self.credential_num)
        foursq_cred_name = '4sq-' + str(self.credential_num)
        oauth_keys = {'consumer_key': config.get(twitter_cred_name, 'consumer_key'),
                      'consumer_secret': config.get(twitter_cred_name, 'consumer_secret'),
                      'access_token_key': config.get(twitter_cred_name, 'access_token_key'),
                      'access_token_secret': config.get(twitter_cred_name, 'access_token_secret')}
        self.foursq_credentials = {'client_id': config.get(foursq_cred_name, 'client_id'),
                                   'client_secret': config.get(foursq_cred_name, 'client_secret'),
                                   'api_version': FOURSQUARE_API_VERSION}
        self.oauth_token = oauth.Token(key=oauth_keys['access_token_key'], secret=oauth_keys['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=oauth_keys['consumer_key'], secret=oauth_keys['consumer_secret'])
        self.credential_num += 1
        if self.credential_num > NUM_TWITTER_CREDENTIALS:
            self.credential_num = self.credential_num % NUM_TWITTER_CREDENTIALS
            if self.credential_num == 0: self.credential_num = 1
        self.num_reconnect = 0

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
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(self.post_params))
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
                                                                             urllib.urlencode(self.post_params)))
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
                # Network error, use linear back off up to 16 seconds
                log('Network error: %s' % self.conn.errstr())
                log('Waiting %s seconds before trying again. Num reconnect: %s' % (backoff_network_error, self.num_reconnect))
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                self.num_reconnect += 1
                if self.num_reconnect > MIN_NUM_RECONNECT:
                    # try again with different twitter credentials
                    self.set_credentials()
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            print sc
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                log('Rate limit, waiting %s seconds' % backoff_rate_limit)
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                log('HTTP error %s, %s' % (sc, self.conn.errstr()))
                log('Waiting %s seconds' % backoff_http_error)
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)

    # Check if this is a Foursquare post and save to foursquare table if so.
    def save_foursquare_data_if_present(self, message):
        entities = message.get('entities')
        if entities and entities.get('urls'):
            print entities
            expanded_urls = [url.get('expanded_url') for url in entities.get('urls')]
            for expanded_url in expanded_urls:
                if "swarmapp.com" in expanded_url or "4sq.com" in expanded_url or "foursquare.com" in expanded_url:
                    try:
                        get_url = "https://api.foursquare.com/v2/venues/search?ll=" \
                                + ",".join([str(f) for f in message['geo']['coordinates']]) \
                                + "&client_id=" + self.foursq_credentials['client_id'] \
                                + "&client_secret=" + self.foursq_credentials['client_secret'] \
                                + "&v=" + self.foursq_credentials['api_version'] 
                        print get_url
                        response = requests.get(get_url).json()
                        if response['meta']['code'] == 200:
                            foursq_data = response['response']
                            matching_venue = {}
                            for place in foursq_data['venues']:
                                if place['name'].lower() in self.html_parser.unescape(message['text'].lower()) \
                                    or ('twitter' in place['contact'] and place['contact']['twitter'].lower() in message['text'].lower()):
                                    matching_venue = place
                                    break
                            if matching_venue:
                                message['foursquare_data'] = {"certain": True, "venues": [matching_venue]}
                            else:
                                foursq_data['certain'] = False
                                message['foursquare_data'] = foursq_data
                            log('Added Foursquare Data: ' + str(message['foursquare_data']))
                    except:
                        log_exception('Failed to add Foursq data to the message.')
                    # db[self.foursquare_col].insert(message)


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
                log('Rate limiting caused us to miss %s tweets' % (message['limit'].get('track')))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                log('Got warning: %s' % message['warning'].get('message'))
            elif message['coordinates'] == None:
                pass # message with no actual coordinates, just a bounding box
            else:
                lon = message['coordinates']['coordinates'][0]
                lat = message['coordinates']['coordinates'][1]
                if lon >= self.min_lon and lon <= self.max_lon and \
                        lat >= self.min_lat and lat <= self.max_lat:
                    # db[self.tweet_col].insert(dict(message))
                    self.save_to_postgres(dict(message))
                    log('Got tweet with text: %s' % message.get('text').encode('utf-8'))
                    # TODO save foursquare data to its own table
                    # self.save_foursquare_data_if_present(message)

        sys.stdout.flush()
        sys.stderr.flush()
        return len(data)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', '-c', required=True,
        help='Which city to get data from.',
        choices=['pgh', 'sf', 'ny', 'chicago', 'houston', 'detroit', 'miami',
            'cleveland', 'seattle', 'london', 'minneapolis'])
    parser.add_argument('--logs_dir', '-l', default='/data/twitter_logs') 
    args = parser.parse_args()

    print "Getting stream in " + args.city

    timestamp = time.time()
    errFile = open(args.logs_dir + '/error_%s_%d.log'%(args.city, timestamp), 'w')
    outFile = open(args.logs_dir + '/output_%s_%d.log'%(args.city, timestamp), 'w')
    sys.stdout = outFile
    sys.stderr = errFile

    ts = TwitterStream(args.city)
    ts.setup_connection()
    ts.start()
