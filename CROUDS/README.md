CROUDS
======

This document started 2015-07-28 by Jinny Kim - hyunjiki@andrew.cmu. 

CROUDS stands for Crowd Reporting of Urban Data Streams.
CROUDS is a branch of Jason Hong and Dan Tasse's [Urban Analytics Project](https://www.hcii.cmu.edu/news/2015/hong-tasse-see-social-media-urban-planning-tool). 


FindUsers.py
------------
Find public Twitter users whose recent tweets were at a specific location point. 

#### Defalt values
- users within **500 meters** from the location point
- tweet made within the last **5 minutes** 
- home (user's most commonly tweeted neighborhood) **not** specified
- tweets made in **City of Pittsburgh, PA**

#### Example queries
- `FindUsers.search(home = 'Central Oakland', location_type = 'venue name', location = 'Jared L. Cohon University Center')`
- `FindUsers.search(minutes_since = 10, location_type = 'venue name', location = 'Jared L. Cohon University Center')`
- `FindUsers.search(location_type = 'venue id', location = '40a55d8dfeee3')`
- `FindUsers.search(location_type = 'streets', location = ('Craig st', 'Forbes ave'))`
- `FindUsers.search(location_type = 'streets', location = ('Craig st', 'Forbes ave'), max_distance='10000', test = True)`

#### Notes

- If a `location` is specified, **location-type** must also be specified: 
	- `venue id`
	- `venue name`
	- `streets`
- In current version **all public Twitter users** in database returned, not just **volunteers**. This can be modified in line 204 of FindUsers.py (is_a_volunteer())
- If `test = True`, the query will instead search for **first 100 tweets it finds** within the last 10 days (for faster querying) made near the location.


ParseTweet.py
------------
Parses a tweet text to extract a number (for numeric type response) or a letter (for multiple-choice type response).

#### To test
Run `tester.py`.
Make sure that ParseTweet-tests.csv is saved as Windows CSV file. 


To run CROUDS flask web app
----------------------------
1. Activate env
2. Run run.py

#### You can
- Add new question (open a question)
- Find users near a location
- View questions in db
- View responses in db


