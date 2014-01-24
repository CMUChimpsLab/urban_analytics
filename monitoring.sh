#!/bin/bash

echo "Current time:"
date
echo "Tweets status:"
mongo tweet --eval "printjson(db.tweet_pgh.stats());"
echo
