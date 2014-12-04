#!/usr/bin/env python

# For each user who answered our survey, gets a count of the bins that that
# user has tweeted in.
# For example, {(40.536, -79.958): 4, (40.329, -80.132): 2, ...}
# Writes it to stdout.

import pymongo, csv, time, json, pprint
from earth_distance import earth_distance_m
from collections import Counter

db = pymongo.MongoClient('localhost', 27017)['tweet']

def round_latlon(lat, lon):
    if not lat or not lon:
        return (None, None)
    return (round(float(lat), 3), round(float(lon), 3))
 
if __name__ == '__main__':
    output_lines = []

    for line in csv.DictReader(open('twitter_home_work_clean.csv', 'rU')):
        screen_name = line['screen_name']
        home_lat = line['home_lat']
        home_lon = line['home_lon']
        work1_lat = line['work1_lat']
        work1_lon = line['work1_lon']
        work2_lat = line['work2_lat']
        work2_lon = line['work2_lon']
        bins = Counter()
        tweets_cursor = db['tweet_pgh'].find({'user.screen_name':screen_name})
        for tweet in tweets_cursor:
            coords = tweet['coordinates']['coordinates']
            lon = coords[0]
            lat = coords[1]
            bins[round_latlon(lat, lon)] += 1

        line['bins_hist'] = bins.values()
        predictions = bins.most_common(2)
        if len(predictions) >= 1:
            # there is a home prediction
            home_prediction = predictions[0][0]
            line['home_prediction_error_m'] = earth_distance_m(float(home_lat), float(home_lon), home_prediction[0], home_prediction[1])
        if len(predictions) >= 2:
            work1_prediction = predictions[1][0]
            line['work1_prediction_error_m'] = earth_distance_m(float(home_lat), float(home_lon), home_prediction[0], home_prediction[1])

        output_lines.append(line)

    print json.dumps(output_lines)
