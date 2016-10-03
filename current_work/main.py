import dbProcess
# import tweet_term, tweet_auto, tweet_temp, dbscan
# import myWordcloud
# import dbProcessWithAll



# TWEET PROCESSING
# *****************************************************************************
# PROCESS VALID TWEETS IN CITY: TWEET_SENTI = TXT_SENTI + EMOJI_SENTI
# build a new database, data pre-processing and store the data into the data base
# ------------------------------------------------------------------------------
#
dbProcess.dbProcess('tweet_pgh_ttt','Neeraj',maxIter=False)