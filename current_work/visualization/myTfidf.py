from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import json

def getKey(item):
    return item[1]

def myTfIdf(para):
  corpus = []
  resultmap = {}
  for i in range(len(para)):
    corpus.append(" ".join(para[i][3]))
  # print corpus[0]
  # print corpus[100]
  # corpus = ["The result from the csv reader is a list",
  #           "lower only works on strings. Presumably it is a",
  #           "list of string, so there are two options. Either you can"]
  vectorizer=CountVectorizer()
  transformer=TfidfTransformer()
  tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
  word=vectorizer.get_feature_names()
  weight=tfidf.toarray()
  for i in range(len(weight)):
    # print u"-----class:",i,u"------"
    resultArr = []
    for j in range(len(word)):
      resultArr.append([word[j],weight[i][j]])
    resultArr.sort(key=getKey,reverse=True)

    if para[i][0] not in resultmap:
      resultmap[para[i][0]] = {}
    if para[i][1] not in resultmap[para[i][0]]:
      resultmap[para[i][0]][para[i][1]] = {}
    if para[i][2] not in resultmap[para[i][0]][para[i][1]]:
      resultmap[para[i][0]][para[i][1]][para[i][2]] = {}
    resultmap[para[i][0]][para[i][1]][para[i][2]]["term"] = []
    resultmap[para[i][0]][para[i][1]][para[i][2]]["value"] = []
    for j in range(15):
      if resultArr[j][1] < 0.01:
        break
      resultmap[para[i][0]][para[i][1]][para[i][2]]["term"].append(resultArr[j][0])
      resultmap[para[i][0]][para[i][1]][para[i][2]]["value"].append(resultArr[j][1])
      # print resultmap[para[i][0]][para[i][1]][para[i][2]]["term"]
  with open('tfidf.json','w') as outfile:
    json.dump(resultmap, outfile)
# mdd =[["tt","tt","tt","The result from the csv reader is a list"],
#       ["tt","tt","tt","lower only works on strings. Presumably it is a"],
#       ["tt","tt","tt","list of string, so there are two options. Either you can"]]
# myTfIdf(mdd)
