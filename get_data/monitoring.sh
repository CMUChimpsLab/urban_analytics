#!/bin/bash

# Note: this is out of date, we have 10 cities getting tweets now
echo "Note: this is out of date, we have 10 cities getting tweets now"
echo "Current time:"
date
echo "Tweets status:"
mongo tweet --eval "printjson(db.tweet_pgh.stats());"
echo "Instagrams status:"
mongo instagram --eval "printjson(db.instagram_pgh.stats());"
echo "Flickrs status:"
mongo flickr --eval "printjson(db.flickr_pgh.stats());"

echo "Note: this is out of date, we have 10 cities getting tweets now"
