db = db.getSiblingDB('tweet');
var tweets = db.runCommand({count: 'tweet_pgh'})['n'];
db = db.getSiblingDB('flickr');
var flickrs = db.runCommand({count: 'flickr_pgh'})['n'];
db = db.getSiblingDB('instagram');
var instagrams = db.runCommand({count: 'instagram_pgh'})['n'];
var currentDate = new Date();
print(currentDate + ',Tweets,' + tweets + ',Flickrs,' + flickrs + ',Instagrams,' + instagrams)
