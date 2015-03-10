*****For Pittsburgh only*****

Given a Twitter username, this map can 
-plot the range of all tweets under that username using a standard deviation ellipse. Some usernames might not work right now because some of the usernames in the user_SDE database do not have the ellipse info (still on circle info).
-plot each individual tweet under that username
-create a heatmap of tweets under that username

This map also can display a heatmap of a sample of tweets in Pittsburgh.

-----------------------------------------------------------------------------
To run this: run ./main.py, then go to localhost:5000 in a browser.

Troubleshooting: If on startup you get:
- ImportError: no module named flask (or something): make sure you're in the
virtualenv (source ../env/bin/activate)
- pymongo.errors.ConnectionFailure: could not connect to localhost:27017: make
sure mongod is running

