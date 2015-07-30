#!/usr/bin/python

import string, psycopg2, requests, json, csv, time
from datetime import datetime, date
from geopy.distance import vincenty

Foursquare_CLIENT_ID = '0015X0KQ1MLXKW0RTDOCOKUMACBCKE30ZY2IFYPCQDYTZ3EC'
Foursquare_CLIENT_SECRET ='UKJRW30YZAXC5DUO5KOZFPM4XWD3O3YSK0ANCZKB3TYCMCA5'

class FindUsers():

    @staticmethod
    def search(  
                minutes_since = 5,
                home = None, 
                location_type = None,
                location = None,
                max_distance = None, 
                test = False
        ): 
        query_start_time = time.time()
        recent_tweeters = get_recent_tweeters(minutes= minutes_since, test= test) 
        if location_type == 'venue name':
            users_at_location = filter_by_venue(users=recent_tweeters,
                                                venue_name=location,
                                                max_distance=max_distance)
        elif location_type == 'venue id':
            users_at_location = filter_by_venue(users=recent_tweeters, 
                                                venue_id=location,
                                                max_distance=max_distance)
        elif location_type == 'streets':
            users_at_location = filter_by_streets(users=recent_tweeters,
                                                streets=location,
                                                max_distance=max_distance)
        else: 
            users_at_location = recent_tweeters

        if home != None:
            users_at_location = filter_by_home(users=users_at_location,  
                                                neighborhood=home)

        volunteers_at_location = get_volunteers(users_at_location)
        elapsed_time = time.time() - query_start_time
        print 'Query took: ' + str(elapsed_time)
        return volunteers_at_location

def get_recent_tweeters(minutes, test):
    query_statement = ("""SELECT DISTINCT ON (user_screen_name) user_screen_name, 
                        ST_AsGeoJSON(coordinates)
                        FROM tweet_pgh 
                        WHERE created_at >= (now() - interval '%s minutes') 
                        ORDER BY user_screen_name, created_at DESC; """ % (minutes))

    if test == True: # for faster query results for testing
        search_limit = 1000
        query_statement = ("""SELECT DISTINCT ON (user_screen_name) user_screen_name, 
                            ST_AsGeoJSON(coordinates)
                            FROM tweet_pgh 
                            WHERE created_at >= (now() - interval '30 days') 
                            ORDER BY  user_screen_name, created_at DESC
                            limit %s; """ % (search_limit))

    conn = psycopg2.connect(database="tweet", user="jinnyhyunjikim")
    cur = conn.cursor()
    cur.execute(query_statement)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    columns = ('username', 'location')
    recent_tweeters = []
    for tweet in result:
        recent_tweeters.append( dict(zip(columns,tweet)) )
    for tweet in recent_tweeters:
        tweet['coordinates'] = get_coordinates(tweet['location']) 
    return recent_tweeters

def filter_by_venue(users, city='PGH', venue_id=None, venue_name=None, max_distance=500):
    # max_distance in meters
    nearby_users = []
    venue_coordinates = get_venue_coordinates(city=city, 
                            venue_id= venue_id, venue_name= venue_name)
    for user in users:
        user_coordinates = user['coordinates']
        distance = vincenty(user_coordinates, venue_coordinates).meters
        if distance <= max_distance:
            nearby_users.append(user)
    return nearby_users

def filter_by_streets(users, streets, max_distance=500):
    # streets = tuple of strings e.g. ('Craig st', 'Forbes ave')
    # max_distance in meters
    street_coords = get_street_coords(streets[0], streets[1])
    nearby_users = []
    for user in users:
        user_coords = user['coordinates']
        distance = vincenty(user_coords, street_coords).meters
        if distance <= max_distance:
            nearby_users.append(user)
    return nearby_users

def filter_by_home(users, neighborhood):
    filtered = []
    for user in users:
        username = user['username']
        home = get_home(username)
        if (home == neighborhood): filtered.append(user)
    return filtered

def get_coordinates(location_str):
    try: 
        start_index = location_str.find('[') + 1
        comma_index = location_str.find(',', start_index)
        end_index = location_str.find(']}')
        longitude = float(location_str[start_index:comma_index])
        latitude = float(location_str[comma_index+1:end_index])
        coordinates = [latitude, longitude]
        return coordinates
    except: 
        # Coordinates of the tweet not found. CMU's as placeholder
        return [40.4433, 79.9436]

def get_street_coords(street_a, street_b):
    street_a = street_a.replace(' ', '+')
    street_b = street_b.replace(' ', '+')
    address = street_a + '+' + street_b 
    API_KEY = 'AIzaSyDmBsLXqP8ClEz8Rx_zK5-0Gow_TIMmWEQ'
    url = """https://maps.googleapis.com/maps/api\
/geocode/json?address=%s,+Pittsburgh,+PA&key=%s""" % (address, API_KEY)
    result = requests.get(url).json()
    result = result['results'][0]['geometry']['location']
    lat, lng = result['lat'], result['lng']
    lat, lng = round(lat, 6), round(lng, 6)
    return (lat, lng)

def get_venue_coordinates(city="PGH", venue_id=None, venue_name=None):
    city_dict = {'PGH': 'pittsburgh,pa', 'NY': 'new+york+city,ny', 
                'SF': 'san+francisco,ca', 'CLEVELAND': 'cleveland,oh', 
                'CHICAGO': 'chicago,illinois', 'SEATTLE': 'seattle,washington', 
                'HOUSTON': 'houston,texas', 'DETROIT': 'detroit,michigan', 
                'MIAMI': 'miami,florida', 'minneapolis': 'minneapolis,minnesota',
                'LONDON': 'london,uk'}
    if city in city_dict.keys(): city_state = city_dict[city] 
    else: print 'City ' + city + ' not available for venue search. '
    today = "{:%Y%m%d}".format(datetime.now())

    if venue_id != None:
        complete_url = ('https://api.foursquare.com/v2/\
venues/%s?client_id=%s&client_secret=%s&v=%s' 
% (venue_id, Foursquare_CLIENT_ID, Foursquare_CLIENT_SECRET, today))
    elif venue_name != None:
        venue_name = venue_name.replace(' ', '+') 
        complete_url = ('https://api.foursquare.com/v2/venues/\
search?query=%s&match=true&near=%s&client_id=%s&client_secret=%s&v=%s' 
%(venue_name, city_state, Foursquare_CLIENT_ID, Foursquare_CLIENT_SECRET, today))
    else: 
        print 'No venue specified.'
        return -1
    response = requests.get(complete_url)
    response = response.json()

    valid = response['meta']['code']
    if valid == 200:
        response = response['response']
        try: first_venue = response['venue']
        except: first_venue = response['venues'][0]
        first_venue_id = first_venue['id']
        first_venue_location = first_venue['location']
        lat = first_venue_location['lat']
        lng = first_venue_location['lng']
        return (lat, lng)
    else: 
        print 'No matching venue found.'
        return -1

def get_home(username):
    query = "SELECT most_common_neighborhood FROM user_pgh WHERE screen_name = '%s' ;" % (username)
    conn = psycopg2.connect(database="tweet", user="jinnyhyunjikim")
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    if len(result) == 0: 
        return 'Home for user:' + username + ' not available.'
    else: 
        home = result[0][0]
        return home

def get_volunteers(users):
    return users
    volunteers = []
    for user in users:
        username = user['username']
        if is_a_volunteer(username) == True:
            volunteers.append(user)
    return volunteers

def is_a_volunteer(username):
    return True ## for testing
    for volunteer in csv.reader(open("static/screen-names.csv")):
        if volunteer[0] == username:
            return True
    return False


