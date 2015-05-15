Trying to use google maps (copy from Andy) to display a map quickly and easily.
Ideally we'd be able to display one user's tweets easily.
This doesn't actually get there, but it does display a map, so that's a start. And puts lines over it. Screenshot in screenshot.png.

Client-side, this uses require.js, which was a new thing to me.
templates/layout.html includes templates/main.html, which includes the script
require.js, while also declaring a data-main attribute of static/js/app.js.
require.js then kicks off in app.js, which requires app/main.js, which requires
app/TweetMap.js and jquery, and so on. Then TweetMap depends on the Google Maps
API, which is how you get that in there.

How does Google Maps know who we are? Hmm...
Short answer: it doesn't. While we're under the usage limits, they don't care
who we are. To deploy to the public, though, we should use an API key. More:
https://developers.google.com/maps/documentation/javascript/tutorial#api_key


To run this: run ./main.py, then go to localhost:5000 in a browser.

Troubleshooting: If on startup you get:
- ImportError: no module named flask (or something): make sure you're in the
virtualenv (source ../env/bin/activate)
- pymongo.errors.ConnectionFailure: could not connect to localhost:27017: make
sure mongod is running

