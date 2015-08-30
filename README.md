# Scripts etc for urban analytics work
Doc updated 2015-08-30

## get_data/

There used to be a folder called `get_data`. It was there to contain all the scripts where we would gather data from social media (twitter, instagram). It's since been moved over to another repo, `scrape_social_media_in_area`.

## analyze/

This is mostly an elephant graveyard by now. It's not useful code so much as a few broken things that you might be able to carve into pieces that you might want later.

- pgh_d3/ includes a couple things: a demo map thing (think of it as map0) and a couple scripts that iterate over the whole DB and try to do something with all the tweets. For example, generate a centroid of each user's tweets. Built on Mongo, probably doesn't work now.
- map1, map2, map3, and map4 are demo maps I tried to make. I don't think they even work anymore. More info in each individual folder.
- radiimap/ is a map that Hong Bin Shim and Jennifer Chou made for various purposes. It was called radiimap because, at one point, it displayed radii of how far various people travel.

This organization scheme is pretty dumb. It should probably be changed at some point. In the meantime, feel free to make a new directory here and copy/paste code from previous maps.
