# Scripts etc for urban analytics work
Doc updated 2015-05-15

Do try to keep this up to date; now that there are multiple people working in this repo, documentation will be more important than it used to be when it all lived in Dan's head. Imagine you're a new developer just looking at all our code for the first time; how would you make sense of it?

## analyze/

- pgh_d3/ includes a couple things: a demo map thing (think of it as map0) and a couple scripts that iterate over the whole DB and try to do something with all the tweets. For example, generate a centroid of each user's tweets. Built on Mongo, probably doesn't work now.
- map1, map2, map3, and map4 are demo maps I tried to make. I don't think they even work anymore. More info in each individual folder.
- radiimap/ is a map that Hong Bin Shim and Jennifer Chou made for various purposes. It was called radiimap because, at one point, it displayed radii of how far various people travel.

This organization scheme is pretty dumb. It should probably be changed at some point. In the meantime, feel free to make a new directory here and copy/paste code from previous maps.

## get_data/

Scripts to download Tweets, Instagrams, and Flickr photos, along with some monitoring stuff, and tools that will help us know if any of our data collection is broken at all. These scripts are basically running 24/7. (at least, the Twitter and Instagram ones are; the Flickr one just ran once to get all historical photos.)

Also `load_tweets_into_postgres` and `load_instagrams_into_postgres`, which are there to transfer all that data from Mongo to PostgreSQL, and are maintained for the functions `tweet_to_insert_string` and `instagram_to_insert_string`, which map between JSON objects from APIs and database rows.
