#!/bin/bash

echo "Current time:"
date
echo "Tweets status:"
mongo tweet --eval "printjson(db.tweet_pgh.stats());"
echo "Instagrams status:"
mongo instagram --eval "printjson(db.instagram_pgh.stats());"
echo "Flickrs status:"
mongo flickr --eval "printjson(db.flickr_pgh.stats());"

