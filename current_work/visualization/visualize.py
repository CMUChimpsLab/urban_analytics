import dbProcess, os, copy
import geoCluster
import getNghd
import json
import myTfidf
from collections import defaultdict
import sqlite3
import gmplot
import re
import getColor
import getCorrectName
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk.tokenize import word_tokenize
import preprocessing as pre
import csv
import geopy
import datetime as dt
import numpy as np

tbname='tweet_pgh_ttt'
dbname='Neeraj'
user='postgres'
pg=dbProcess.PgController(tbname,dbname,user)

topicbase = [
    ['traffic', 'transport', 'bus', 'escort', 'shuttle', 'megabus', 'taxi', 'uber',
     'lyft', 'authority', 'cab', 'port', 'intersection', 'highway', 'drive', 'transportation',
     '71d', 'avenue', 'driveway', 'lane', 'drove'],
    ['noise', 'noisy', 'quiet', 'loudly', 'loud', 'beep', 'louder', 'silence'],
    ['neighbor', 'neighborhood'],
    ['plaza', 'apartment', 'dorm', 'bedroom'],
    ['shopping', 'market', 'purchase', 'sale', 'wholesale', 'outlet', 'store', 'discount', 'vendor',
     'coupon', 'grocery', 'walmart', 'retail', 'mall', 'procurement', 'nordstrom'],
    ['banquet', 'dine', 'restaurant', 'cafeteria', 'cafe', 'eatery', 'pizzeria', 'ristorante', 'cuisine',
     'steakhouse', 'deli', 'qdoba', 'pasta', 'sushi', 'primantis', 'toast', 'grill', 'delicious', 'menu',
     'chili', 'noodlehead', 'burrito', 'primanti', 'burger', 'bakery', 'cakery', 'spaghetti', 'roast',
     'hibachi', 'falafel', 'dibellas', 'coleslaw', 'chilly', 'brueggers', 'pierogies',
     'tapa', 'schmicks', 'seafood', 'mccormick'],
    ['beer', 'cocktail', 'liquor', 'pub', 'bar', 'wine', 'champagne', 'gin', 'vodka', 'martini',
     'whiskey', 'ale', 'lager', 'alcohol', 'tequila', 'tavern', 'bartender', 'hoppy', 'pilsner',
     'bourbon', 'rum', 'fuddle', 'mead', 'yuengling', 'margarita'],
    ['criminal', 'arrest', 'assault', 'robbery', 'shooting', 'crime', 'violent', 'perp', 'gun', 'drag',
     'safety', 'steal'],
    ['basketball', 'nba', 'ballpark', 'coach', 'superbowl', 'baseball', 'hockey', 'ncaa', 'coached',
     'football', 'rebound', 'nfl', 'steeler', 'pitcher', 'tennis', 'golf', 'couch', 'tournament',
     'steelers', 'soccer', 'espn', 'athletics', 'stadium', 'steelersnation', 'mlb', 'dunk'],
    ['therapy', 'surgery', 'lifecare', 'ward', 'upmc', 'medic', 'doctor', 'medicine', 'dentist',
     'patient', 'nursing', 'icu', 'hospital', 'clinical'],
    ['garbage', 'trash', 'scum']
    ]
textFormulate = getCorrectName.GetCorrectName()

totalTopics = 11
topicarr = ['transportation', 'sound', 'neighborhood', 'apartment', 'shopping', 'eating', 'drinking', 'safety',
         'sports', 'health', 'garbage']
samplegran = [27, 10, 6, 10, 46, 57, 90, 18, 102, 20, 6]
nghdmap = getNghd.Getnghd()
nghdNameLst = nghdmap.getnghdName()
resultArr = {}
termNghdTopicSenti = {}

tweets_per_topic = defaultdict(lambda: defaultdict(list))
topicJson = {}
topicJsonSenti = {}
for topic in topicarr:
    topicJson[topic] = []
    topicJsonSenti[topic] = {}
    for nghd in nghdNameLst:
        topicJsonSenti[topic][nghd] = {}
        topicJsonSenti[topic][nghd]["count"] = 0
        topicJsonSenti[topic][nghd]["poscnt"] = 0
        topicJsonSenti[topic][nghd]["possenti"] = 0
        topicJsonSenti[topic][nghd]["negcnt"] = 0
        topicJsonSenti[topic][nghd]["negsenti"] = 0

for nghd in nghdNameLst:
    resultArr[nghd] = {}
    termNghdTopicSenti[nghd] = {}
    resultArr[nghd]["topics"] = copy.deepcopy(topicarr)
    resultArr[nghd]["topic data"] = {}
    for topicIter in topicarr:
        termNghdTopicSenti[nghd][topicIter] = {}
        termNghdTopicSenti[nghd][topicIter]["positive"] = []
        termNghdTopicSenti[nghd][topicIter]["negative"] = []
        resultArr[nghd]["topic data"][topicIter] = {}
        resultArr[nghd]["topic data"][topicIter]["count"] = 0
        resultArr[nghd]["topic data"][topicIter]["value"] = 0
        resultArr[nghd]["topic data"][topicIter]["poscnt"] = 0
        resultArr[nghd]["topic data"][topicIter]["negcnt"] = 0
        resultArr[nghd]["topic data"][topicIter]["color"] = "#000000"

IDarr = {}
for i in range(totalTopics):
    fdarr = open(format("../txt/tweetClass%d.txt" % i),"r")
    for j in range(samplegran[i]*100):
        line = fdarr.readline()
        # print line
        line = line.split()
        if line[0] not in IDarr:
            IDarr[line[0]] = i
    fdarr.close()

gmap = [gmplot.GoogleMapPlotter(40.45, -79.89, 11) for i in range(totalTopics)]
gmap2 = [gmplot.GoogleMapPlotter(40.45, -79.89, 11) for i in range(24)]

senti_val_sum = [ [ 0 for i in range(totalTopics) ] for j in range(18) ]
senti_val_count = [ [ 0 for i in range(totalTopics) ] for j in range(18) ]
cnt = 0
tweetDup = {}

pg.cur.execute('''
	select id,senti_val,lon,lat,txt,term,hour
	from %s where auto_tweet is Null;'''%pg.tbname)
for (id,senti_val,lon,lat,txt,term,thehour) in pg.cur.fetchall():
    if id not in IDarr:
        continue
    if abs(senti_val)<0.001:
        continue
    if id in tweetDup:
        continue
    topicJson[topicarr[IDarr[id]]].append([lat, lon, getColor.getColor(senti_val)])
    tweetDup[id] = 1
    cnt += 1
    txtarr = txt.split()
    term = term.split(",")
    if cnt%500 == 0:
        print cnt
    nghdName = nghdmap.getnghd((lat,lon))
    if senti_val > 0:
        resultArr[nghdName]["topic data"][topicarr[IDarr[id]]]["poscnt"] += 1
        termNghdTopicSenti[nghdName][topicarr[IDarr[id]]]["positive"].extend(term)
        topicJsonSenti[topicarr[IDarr[id]]][nghdName]["poscnt"] += 1
        topicJsonSenti[topicarr[IDarr[id]]][nghdName]["possenti"] += senti_val
    else:
        resultArr[nghdName]["topic data"][topicarr[IDarr[id]]]["negcnt"] += 1
        termNghdTopicSenti[nghdName][topicarr[IDarr[id]]]["negative"].extend(term)
        topicJsonSenti[topicarr[IDarr[id]]][nghdName]["negcnt"] += 1
        topicJsonSenti[topicarr[IDarr[id]]][nghdName]["negsenti"] += senti_val
    resultArr[nghdName]["topic data"][topicarr[IDarr[id]]]["count"] += 1
    resultArr[nghdName]["topic data"][topicarr[IDarr[id]]]["value"] += senti_val
    topicJsonSenti[topicarr[IDarr[id]]][nghdName]["count"] += 1


    for i in range(len(term)):
        theTerm = textFormulate.getName(term[i])
        if (theTerm in topicbase[IDarr[id]]):
            theRawTerm = process.extract(theTerm,choices=txtarr, limit=3)
            for j in range(len(theRawTerm)):
                # print theRawTerm[j][0]
                # print theRawTerm[j][1]
                # print "----------------"
                if theRawTerm[j][1]<91:
                    continue
                for k in range(len(txtarr)):
                    # print theRawTerm[j][0]
                    # print txtarr[i]
                    if theRawTerm[j][0] == txtarr[k]:
                        txtarr[k] = "<b>"+ txtarr[k] + "</b>"

    txt = " ".join(txtarr)
    tweets_per_topic[nghdName][topicarr[IDarr[id]]].append(format("%s&a*a&%0.4f&a*a&%s"%(txt,senti_val,','.join(term))))
    gmap[IDarr[id]].scatter([lat], [lon], getColor.getColor(senti_val), size=40, marker=False)

    thehour = (thehour + 24 - 7) % 24
    if IDarr[id] == 0:
        # print thehour
        gmap2[thehour].scatter([lat], [lon], getColor.getColor(senti_val), size=40, marker=False)

for i in range(totalTopics):
    gmap[i].draw(format("../map/map_%s.html"%topicarr[i]))


for nghd in resultArr:
    for topicIter in topicarr:
        if resultArr[nghd]["topic data"][topicIter]["count"] != 0:
            resultArr[nghd]["topic data"][topicIter]["value"] /= resultArr[nghd]["topic data"][topicIter]["count"]
            tmppppp = getColor.getColor(resultArr[nghd]["topic data"][topicIter]["value"])
            resultArr[nghd]["topic data"][topicIter]["color"] = tmppppp
            # resultArr[nghd]["topic data"][topicIter]["color"] = getColor.getColor(resultArr[nghd]["topic data"][topicIter]["value"])
        else:
            del resultArr[nghd]["topic data"][topicIter]
            resultArr[nghd]["topics"].remove(topicIter)
with open('..//json//nghd_words.json','w') as outfile:
    json.dump(resultArr, outfile)
with open('..//json//tweets_per_nghd_words.json','w') as outfile:
    json.dump(tweets_per_topic,outfile, indent=2)
with open('..//json//tweets_per_topic.json','w') as outfile:
    json.dump(topicJson,outfile, indent=2)
with open('..//json//tweets_per_topic_senti.json','w') as outfile:
    json.dump(topicJsonSenti,outfile, indent=2)

# get word cloud data
# termPara = []
# print nghdNameLst
# for nghd in nghdNameLst:
#     for topicIter in topicarr:
#         # print "--------"
#         if len(termNghdTopicSenti[nghd][topicIter]["positive"]) > 0:
#             termPara.append([nghd,topicIter, "positive", termNghdTopicSenti[nghd][topicIter]["positive"]])
#         if len(termNghdTopicSenti[nghd][topicIter]["negative"]) > 0:
#             termPara.append([nghd,topicIter, "negative", termNghdTopicSenti[nghd][topicIter]["negative"]])
# myTfidf.myTfIdf(termPara)





label = ['transportation', 'sound', 'neighborhood', 'house', 'shopping', 'eating', 'drinking', 'safety',
         'sports', 'health', 'garbage']
