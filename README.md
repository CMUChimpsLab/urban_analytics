# Scripts etc for urban analytics work
Doc updated 2014-10-11

Do try to keep this up to date; now that there are multiple people working in this repo, documentation will be more important than it used to be when it all lived in Dan's head. Imagine you're a new developer just looking at all our code for the first time; how would you make sense of it?

## analyze/

map1, map2, and map3 are demo maps I tried to make. I don't remember what they each even do anymore.  
pgh_d3/ includes a couple things: a demo map thing (think of it as map0) and a couple scripts that iterate over the whole DB and try to do something with all the tweets. For example, generate a centroid of each user's tweets.  
This organization scheme is pretty dumb. It should probably be fixed.

## get_data/

Scripts to download Tweets, Instagrams, and Flickr photos, along with some monitoring stuff, and tools that will help us know if any of our data collection is broken at all. These scripts are basically running 24/7. (at least, the Twitter and Instagram ones are; the Flickr one just ran once to get all historical photos.)