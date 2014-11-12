#!/usr/bin/env python

# Take in the CSV of responses from the home/work study and check if they're
# in the common_tweeters file. If not, spit them out.
# Outputs a "cleaned up" data set.

# Warning! Calls the Google geocoding API. Don't get rate limited.

import csv, time, argparse
from pygeocoder import Geocoder

# If there are problems with the geocoding, including multiple results, or not
# being in/near Pittsburgh, returns False *and prints out the errors*.
# If there are no problems, returns True.
def is_geocoding_ok(geocode_results):
    if len(geocode_results) > 1:
        print "error: multiple geocode results"
        return False
    if geocode_results[0].state != 'Pennsylvania':
        print "error: not in PA"
        return False
    return True

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--delay', '-d', default=5, type=int)
    parser.add_argument('--outfile', '-o', default='twitter_home_work_clean.csv')
    parser.add_argument('--common_tweeters_file', '-c', default='common_tweeters.csv')
    args = parser.parse_args()

    # common_tweeters: a list of LOWERCASE people in our data set.
    common_tweeters = [line[1].lower() for line in csv.reader(open(args.common_tweeters_file))]
    # already_cleaned names: people who we've already written out; no need to
    # go through them again.
    already_cleaned_names = [line[1].lower() for line in csv.reader(open(args.outfile))]

    outwriter = csv.writer(open(args.outfile, 'a'))

    headers = ['date', 'screen_name', 'age', 'gender', 'home', 'home_clean',
        'home_lat', 'home_lon', 'work', 'work_clean', 'work_lat', 'work_lon',
        'third_places', 'commute']
    outwriter.writerow(headers)

    reader = csv.reader(open('twitter_home_work_responses.csv'))
    next(reader) # to skip header row
    for line in reader:
        date = line[0]
        screen_name = line[1]
        if screen_name.lower() not in common_tweeters:
            print 'bad user: ' + screen_name
            continue
        age = int(line[2])
        gender = line[3]
        home_addr = line[4]
        home_geocode_results = Geocoder.geocode(home_addr)
        if not is_geocoding_ok(home_geocode_results):
            print screen_name
            continue
        home_clean = home_geocode_results[0].formatted_address
        home_lat = home_geocode_results[0].coordinates[0]
        home_lon = home_geocode_results[0].coordinates[1]

        work_addr = line[6]
        work_geocode_results = Geocoder.geocode(work_addr)
        if not is_geocoding_ok(work_geocode_results):
            print screen_name
            continue
        work_clean = work_geocode_results[0].formatted_address
        work_lat = work_geocode_results[0].coordinates[0]
        work_lon = work_geocode_results[0].coordinates[1]
        
        # TODO process third places better
        third_places = line[10]
        commute = line[11]

        outwriter.writerow([date, screen_name, age, gender, home_addr,
            home_clean, home_lat, home_lon, work_addr, work_clean, work_lat,
            work_lon, third_places, commute])

        time.sleep(args.delay)
        

        # print geocode_results[0].state
        # print geocode_results[0].coordinates

