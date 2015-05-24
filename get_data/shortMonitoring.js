// Run with "mongo shortMonitoring.js"
// just gives a quick count of how many tweets in each table.
db = db.getSiblingDB('tweet');
var tweet_pgh = db.tweet_pgh.count();
var tweet_sf = db.tweet_sf.count();
var tweet_ny = db.tweet_ny.count();
var tweet_houston = db.tweet_houston.count();
var tweet_cleveland = db.tweet_cleveland.count();
var tweet_seattle = db.tweet_seattle.count();
var tweet_miami = db.tweet_miami.count();
var tweet_detroit = db.tweet_detroit.count();
var tweet_chicago = db.tweet_chicago.count();
var tweet_london = db.tweet_london.count();
var tweet_minneapolis = db.tweet_minneapolis.count();
db = db.getSiblingDB('flickr');
var flickrs = db.runCommand({count: 'flickr_pgh'})['n'];
db = db.getSiblingDB('instagram');
var instagrams = db.runCommand({count: 'instagram_pgh'})['n'];
var currentDate = new Date();
print(currentDate + ',' + tweet_pgh + ',' + tweet_sf +
    ',' + tweet_ny + ',' + tweet_houston +
    ',' + tweet_cleveland + ',' + tweet_seattle +
    ',' + tweet_miami + ',' + tweet_detroit +
    ',' + tweet_chicago + ',' + tweet_london +
    ',' + flickrs + ',' + instagrams + ',' + tweet_minneapolis)
