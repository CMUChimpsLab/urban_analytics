import dbProcess, os, copy
import re
# import geoCluster
import preprocessing as pre
import gensim
import math
import csv
import geopy
import datetime as dt
import numpy as np

tbname='tweet_pgh_ttt'
dbname='Neeraj'
user='postgres'
pg=dbProcess.PgController(tbname,dbname,user)

def getKey(item):
    return item[2]
def getKey1(item):
    return item[1]

TagTweetFilter = set(['Job:', 'Jobs', 'Hiring','Job'])
emptySet = set()
meanRelevance = [0.183394905466, 0.141034503178, 0.0994776931848, 0.105091033286, 0.157039995027, 0.205406544982,
                 0.189770089465, 0.150936553588, 0.193376499649, 0.16593184442, 0.107548596863]
stdRelevance = [0.0703412438695, 0.0602042883066, 0.0851655390275, 0.0773368657177, 0.0659111055722, 0.0850321877945,
                0.072594593864, 0.0521722375864, 0.0753339787958, 0.0641161889159, 0.06413255081]
cateRatio = [6.56130103955, 6.73311241397, 6.97336683417, 6.3638787071, 6.63194220473, 5.56767859344,
             5.81133189062, 7.13275804846, 5.98627338631, 6.06494708995, 6.92753623188]
biasRelavance = [0.15789473684219, 0.1473980686696, 0.1446957027558, 0.14335166400109, 0.16909115474699,
                 0.163767464486, 0.13005700370805, 0, 0, 0, 0]
samplegran = [27, 10, 6, 10, 46, 57, 90, 18, 102, 20, 6]
meanRelevanceTmp = meanRelevance
for ii in range(len(meanRelevanceTmp)):
    meanRelevance[ii] = meanRelevanceTmp[ii] + (1 + stdRelevance[ii]) / cateRatio[ii]

wordFreq = {}
freqFd = open("..//txt//freq.txt")
while True:
    line = freqFd.readline()
    if line:
        line = line.split()
        wordFreq[line[0]] = int(line[1])
    else:
        break
freqFd.close()


model = gensim.models.Word2Vec.load('../keywordsSelection/modelOut.txt')
for currentTopicId in range(11):
    fd = open(format("../txt/wordSimilarity%d.txt" % currentTopicId),"r")
    wordRelevance = {}
    outputResult = []
    while True:
        line = fd.readline()
        if line:
            line = line.split()
            if len(line) < 2:
                continue
            wordRelevance[line[0]] = float(line[1])
        else:
            break
    fd.close()

    # run the code


    distribute = []
    cntTweet = 0
    refcnt = 0
    othercnt = 0
    pg.cur.execute('''
        select id,senti_val,lon,lat,txt,term,tag
        from %s where auto_tweet is Null;'''%pg.tbname)
    for (id,senti_val,lon,lat,txt,term,hstag) in pg.cur.fetchall():
        # if math.fabs(senti_val)<0.0001:
        #     continue
        cntTweet += 1
        temprelavance = 0
        addcnt = 0
        appeared = False
        term = term.split(",")
        n1 = 0
        n2 = 0
        decreaseFactor = 0
        termplus = []
        for iteri in term:
            if iteri in wordFreq:
                termplus.append([iteri, wordFreq[iteri]])
                if wordFreq[iteri]>0.95:
                    n1 += 1
                else:
                    n2 += 1
        if n2 > 0:
            decreaseFactor = meanRelevance[currentTopicId]+3/math.sqrt(n2)*stdRelevance[currentTopicId]
        # termplus.sort(key=getKey1)
        for i in range(0,len(termplus)):
            if termplus[i][1] > 15000:
                continue
            if termplus[i][0] in wordRelevance:
                addcnt += 1
                temprelavance += (wordRelevance[termplus[i][0]] - meanRelevance[currentTopicId])
                if wordRelevance[termplus[i][0]] > 0.8:
                    appeared = True
        if addcnt == 0:
            addcnt = 1
        if appeared == False:
            temprelavance -= 10
            continue
        # if len(re.findall('\(#[\s\S]+, [\s\S]+\)',txt))>0:
        #     continue
        if hstag != None:
            hstag = hstag.split('#')
            if TagTweetFilter.intersection(hstag) != emptySet:
                continue

        for i in range(0,len(termplus)):
            if termplus[i][0] in wordRelevance:
                if wordRelevance[termplus[i][0]] > 0.95:
                    refcnt +=1
                else:
                    othercnt += 1
                if wordRelevance[termplus[i][0]]<0.95:
                    distribute.append(wordRelevance[termplus[i][0]])
        outputResult.append([id,txt,temprelavance])
    outputResult.sort(key=getKey,reverse=True)
    print refcnt
    print othercnt
    print othercnt * 1.0 / refcnt

    print np.mean(distribute)
    print np.std(distribute)
    print "*******************"
    distribute = np.asarray(distribute)

    # DistributionPlot.myRadarplot(distribute,'''distributionFreq%d'''%currentTopicId)


    writed = {}
    outputfd = open(format("../txt/tweetClass%d.txt" % currentTopicId),"w")
    outputfd2 = open(format("../txt/tweetTest%d.txt" % currentTopicId),"w")
    testcnt = 0
    for tt in outputResult:
        if tt[0] not in writed:
            if testcnt % samplegran[currentTopicId] == 0:
                outputfd2.write("%s %s %f\n"%(tt[0],tt[1],tt[2]))
            testcnt+=1
            outputfd.write("%s %s %f\n"%(tt[0],tt[1],tt[2]))
            writed[tt[0]] = 1
    outputfd.close()
    outputfd2.close()