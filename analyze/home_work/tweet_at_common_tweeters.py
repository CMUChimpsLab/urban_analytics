#!/usr/bin/env python

# Sends tweets to people to invite them to join our study!
# Reads login info from config.txt.

import argparse, csv, ConfigParser, pprint, urllib, time
import oauth2 as oauth

config = ConfigParser.ConfigParser()
config.read('config.txt')
POST_URL = 'https://api.twitter.com/1.1/statuses/update.json'
OAUTH_KEYS = {'consumer_key': config.get('twitter', 'consumer_key'),
              'consumer_secret': config.get('twitter', 'consumer_secret'),
              'access_token_key': config.get('twitter', 'access_token_key'),
              'access_token_secret': config.get('twitter', 'access_token_secret')}

# Given a screen name (without @), sends a recruitment tweet to that user, if
# |actually_send| is True. Otherwise prints to stdout.
# Returns True iff actually sent a tweet, false otherwise.
def send_recruitment_tweet(screen_name, actually_send):
    params = {
        'status': '@' + screen_name + ' Hi! Saw you tweeted in Pgh. Would you mind taking a voluntary 5min CMU survey? Must be 18+. https://docs.google.com/forms/d/1MtRdolCodDVPP9IWYKDmAUYRCHq2VL_Es_T7xglEP7A/viewform',
    }
    post_body=urllib.urlencode(params)

    if not actually_send:
        print "Would send: " + post_body
        return False

    (resp, content) = oauth_req(POST_URL, http_method="POST", post_body=post_body)
    
    print "Sent: " + post_body
    if resp['status'] == '200' and 'errors' not in content:
        return True
    else:
        print "Request Failed"
        pprint.pprint(resp)
        pprint.pprint(content)
        return False

# Sends an actual request to Twitter, with authentication.
# Note! It sends an actual request to Twitter!
def oauth_req(url, http_method="GET", post_body=None, http_headers=None):
    consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
    token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
    client = oauth.Client(consumer, token)
    if http_method == "POST":
        resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    else:
        resp, content = client.request(url, method=http_method, headers=http_headers)
    return (resp, content)

# Given a path to a file containing some common tweeters, returns a dict of
# user -> num_tweets.
def get_tweeters(tweeters_filename):
    retval = {}
    for row in csv.reader(open(tweeters_filename)):
        retval[row[1]] = int(row[2])
    return retval

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tweeters_filename', '-f', default='common_tweeters.csv')
    parser.add_argument('--already_tweeted_filename', '-a', default='already_tweeted.csv')
    parser.add_argument('--really_tweet', '-r', action='store_true', help='Whether to actually tweet at people, or just print to stdout for debugging.')
    parser.add_argument('--number_to_recruit', '-n', type=int, required=True)
    args = parser.parse_args()

    tweeters = get_tweeters(args.tweeters_filename)

    # Remove anyone who's in the already_tweeted file.
    already_sent = [row[0] for row in csv.reader(open(args.already_tweeted_filename)) if row]
    print "Already sent to: " + str(already_sent)
    for tweeter in already_sent:
        if tweeter in tweeters:
            del tweeters[tweeter]

    # get a list of the top N tweeters
    tweeters = sorted(tweeters, key = tweeters.get, reverse=True)[0: args.number_to_recruit]

    already_tweeted_file = open(args.already_tweeted_filename, 'a') # for writing

    print "Going to send to these tweeters: " + str(tweeters)
    time.sleep(10)
    for tweeter in tweeters:
        tweet_worked = send_recruitment_tweet(tweeter, args.really_tweet)
        if tweet_worked:
            already_tweeted_file.write(tweeter + '\n')
        time.sleep(60)

    already_tweeted_file.close()

