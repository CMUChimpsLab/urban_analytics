Scripts to build up the "user" table based on tweets. For example, telling the
number of tweets a user has, or the centroid of all their tweets.

build_user_coll_sde is for building the "standard deviation ellipses" of each
person's path. This and build_user_collection should probably be put together
someday.

Worked only on Mongo. To do this in Postgres, if you want to, you'd have to
basically rewrite the script.
