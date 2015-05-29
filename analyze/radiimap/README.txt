*****For Pittsburgh only*****

-plot the range of all tweets under given username using a standard deviation ellipse. Some usernames might not work right now because some of the usernames in the user_SDE database do not have the ellipse info (still on circle info).
-plot each individual tweet under that username
-create a heatmap of tweets under that username
-plot tweets and the number of tweets based on different neighborhoods (uses 'point_map.csv') also provides UI to show/hide certain neighborhoods.
-create a heatmap of number of unique users in each bin. Each bin rounded to the third decimal. (uses 'bins_num_tweets.csv')
-display frequencies of different types of venues within each bin and the number of unique users in that bin (uses '/nghd_info/outputs/bins_uniq_user_venue.json')

This map also can display a heatmap of a sample of tweets in Pittsburgh.

-----------------------------------------------------------------------------
To run this: run ./main.py, then go to localhost:5000 in a browser.

Troubleshooting: If on startup you get:
- ImportError: no module named flask (or something): make sure you're in the
virtualenv (source ../env/bin/activate)
- pymongo.errors.ConnectionFailure: could not connect to localhost:27017: make
sure mongod is running

