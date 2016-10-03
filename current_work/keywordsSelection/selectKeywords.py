import gensim
import sys
model = gensim.models.Word2Vec.load('modelOut.txt')
while (1):
    print "input a bag of keywords (split with whitespace)"
    line = sys.stdin.readline()
    line = line.split()
    print model.most_similar(positive=line, topn=10)
