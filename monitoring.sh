#!/bin/bash

echo "Tweets status:"
mongo tweet --eval "printjson(db.tweet_pgh.stats());"


