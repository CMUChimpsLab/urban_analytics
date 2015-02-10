*****For Pittsburgh only*****

Given a Twitter username, this map can plot the range (centroid,50%,90% radii) of all tweets under that username. Some usernames might not work right now because some of the usernames in the user_SDE database do not have the ellipse info (still on circle info).

This map also can display a heatmap of a random sample of tweets in Pittsburgh.




To run this: run ./main.py, then go to localhost:5000 in a browser.

Troubleshooting: If on startup you get:
- ImportError: no module named flask (or something): make sure you're in the
virtualenv (source ../env/bin/activate)
- pymongo.errors.ConnectionFailure: could not connect to localhost:27017: make
sure mongod is running

