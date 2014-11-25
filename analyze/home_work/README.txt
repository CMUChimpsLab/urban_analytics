This folder is for things that are part of the study where we try to tell where
people's home and work addresses are based on their geotagged tweets.

already_tweeted.csv is just a file, one line per element, for twitter IDs of
people we've already tried to recruit, so we make sure not to hit them again.
does_not_exist.csv is a list of people who are in our data set but have since
deactivated their accounts.

common_tweeters.csv is all the people we might tweet to.
tweet_at_common_tweeters.py is the script that actually sent out the tweets.

twitter_home_work_responses.csv (and the _backup) are just copies from the
Google doc. twitter_home_work_clean.csv is after removing spammers, cleaning
up data, and geocoding it (done w/ clean_add_geocodes.py).

pull_out_tweets.py took all the users from twitter_home_work_clean from the db,
got all their tweets, and stuck them in a json file (tweets.json).
