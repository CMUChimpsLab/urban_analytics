#!/usr/bin/env python

# Take in the CSV of responses from the home/work study and check if they're
# in the common_tweeters file. If not, spit them out.
# Outputs a "cleaned up" data set.

# Warning! Calls the Google geocoding API. Don't get rate limited.

import csv, time, argparse, os
from earth_distance import earth_distance_m
from pygeocoder import Geocoder
from pygeolib import GeocoderError

# If there are problems with the geocoding, including zero or multiple results,
# or not being in/near Pittsburgh, prints out the errors and the username.
# Returns (formatted address, lat, lon) all as strings. (empty strings if there
# are any errors.)
def geocode_catch_errors(address):
    if address.strip() == '':
        return ('','','')

    try:
        geocode_results = Geocoder.geocode(address)
        if len(geocode_results) > 1:
            print "error: multiple geocode results for: " + ' '.join(address.splitlines())
            return ('', '', '')
        if geocode_results[0].state != 'Pennsylvania':
            print "error: not in PA: " + ' '.join(address.splitlines())
            # Don't return empties, still worth having the geocode I guess
        
        # if distance from center of pittsburgh is > 100 km, also flag it
        dist_from_pgh = earth_distance_m(40.441667, -80,
                float(geocode_results[0].coordinates[0]),
                float(geocode_results[0].coordinates[1]))
        if dist_from_pgh > 100 * 1000:
            print "error: distance over 100 km. address: %s, distance: %d" %\
                (' '.join(address.splitlines()), dist_from_pgh)
        home_clean = geocode_results[0].formatted_address
        home_lat = geocode_results[0].coordinates[0]
        home_lon = geocode_results[0].coordinates[1]
        return (home_clean, home_lat, home_lon)

    except GeocoderError as ge:
        print ge
        return ('','','')
        

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
    already_cleaned_names = []
    if os.path.exists(args.outfile):
        already_cleaned_names = [line[1].lower() for line in csv.reader(open(args.outfile, 'r+'))]
        print "skipping these names, already cleaned: " + str(already_cleaned_names)
        outwriter = csv.writer(open(args.outfile, 'a'))
    else:
        outwriter = csv.writer(open(args.outfile, 'w'))
        headers = ['date', 'screen_name', 'age', 'gender', 'home_addr',
            'home_clean', 'home_lat', 'home_lon', 'time_at_home_addr',
            'work1_addr', 'work1_clean', 'work1_lat', 'work1_lon',
            'work2_addr', 'work2_clean', 'work2_lat', 'work2_lon',
            'is_unemployed', 'is_multiple_jobs', 'is_mobile_work', 'other_places',
            'other1_addr', 'other1_clean', 'other1_lat', 'other1_lon',
            'other2_addr', 'other2_clean', 'other2_lat', 'other2_lon',
            'other3_addr', 'other3_clean', 'other3_lat', 'other3_lon',
            'commute']
        outwriter.writerow(headers)

    reader = csv.reader(open('twitter_home_work_responses.csv'))
    next(reader) # to skip header row
    for line in reader:
        date = line[0]
        screen_name = line[1]
        if screen_name.lower() not in common_tweeters:
            print 'bad user: ' + screen_name
            continue
        if screen_name.lower() in already_cleaned_names:
            print 'already did: ' + screen_name
            continue
        print screen_name
        age = int(line[2])
        gender = line[3]

        home_addr = line[4]
        (home_clean, home_lat, home_lon) = geocode_catch_errors(home_addr)

        time_at_home_addr = line[5]

        work1_addr = line[6]
        (work1_clean, work1_lat, work1_lon) = geocode_catch_errors(work1_addr)

        work2_addr = line[7]
        (work2_clean, work2_lat, work2_lon) = geocode_catch_errors(work2_addr)
       
        is_unemployed = line[8].lower() == 'yes'
        is_multiple_jobs = line[9].lower() == 'yes'
        is_mobile_work = line[10].lower() == 'yes'

        other_places = line[11]
        other1_addr = line[12]
        (other1_clean, other1_lat, other1_lon) = geocode_catch_errors(other1_addr)
        other2_addr = line[13]
        (other2_clean, other2_lat, other2_lon) = geocode_catch_errors(other2_addr)
        other3_addr = line[14]
        (other3_clean, other3_lat, other3_lon) = geocode_catch_errors(other3_addr)

        commute = line[15]

        outwriter.writerow([date, screen_name, age, gender, home_addr,
            home_clean, home_lat, home_lon, time_at_home_addr,
            work1_addr, work1_clean, work1_lat, work1_lon,
            work2_addr, work2_clean, work2_lat, work2_lon,
            is_unemployed, is_multiple_jobs, is_mobile_work, other_places,
            other1_addr, other1_clean, other1_lat, other1_lon,
            other2_addr, other2_clean, other2_lat, other2_lon,
            other3_addr, other3_clean, other3_lat, other3_lon,
            commute])

        time.sleep(args.delay)
 
