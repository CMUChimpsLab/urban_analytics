CROUDS: Crowd Reporting of Urban Data Streams
=========

This document started 2015-07-28 by Jinny Kim - hyunjiki@andrew.cmu. 

CROUDS is a branch of Jason Hong and Dan Tasse's [Urban Analytics](https://www.hcii.cmu.edu/news/2015/hong-tasse-see-social-media-urban-planning-tool) Project. 

Running
-------

Requirements:
- You must have connection to CMU Chimp Lab's Twitter database.
- You must 

FindUsers.py
------------
Finds Twitter users whose recent tweets were made at specific points of interest. 

### Defalt values:
- distance range of **500 meters** 
- recency of the time since the last tweetis are **5 minutes** 
- home (most commonly tweeted neighborhood of the user) specification **none**
- city of **Pittsburgh, PA**

### Example queries:
- FindUsers.search(home = 'Central Oakland', location_type = 'venue name', location = 'Jared L. Cohon University Center')
- FindUsers.search(minutes_since = 10, location_type = 'venue name', location = 'Jared L. Cohon University Center')
- FindUsers.search(location_type = 'venue id', location = '40a55d8dfeee3')



- FindUsers.search(location_type = 'streets', location = )

### Notes:

- If a location is specified, location-type must also be specified: 
	- 'venue id' 
	- 'venue name' 
	- 'streets'
- As there are only a limited number of volunteers within Summer REU interns, current query returns all public Twitter users, not all volunteers, but **volunteer filter** can be switched on in line _____ of FindUsers.py


-max distance ****


ParseTweet.py
------------



AddQuestion.py
------------

