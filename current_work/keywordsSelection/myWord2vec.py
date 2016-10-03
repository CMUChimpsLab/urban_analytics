import gensim, logging
import sys
import os
from sklearn.cluster import KMeans
import numpy as np

# import gensim.models.word2vec

class MySentences(object):
    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):
        for line in open(self.fname):
            yield line.split()

sentences = MySentences('./termWord.txt') # a memory-friendly iterator
# model = gensim.models.Word2Vec(min_count=10, workers=4, size=200)
# model.build_vocab(sentences)
# model.train(sentences)
model = gensim.models.Word2Vec(sentences,min_count=10, workers=4, size=200)
model.save('modelOut.txt')