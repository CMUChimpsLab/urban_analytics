from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.tag.perceptron import PerceptronTagger
from nltk.corpus import wordnet
import chardet
class GetCorrectName():
    def __init__(self):
        self.lmtzr=WordNetLemmatizer()
        self.tagger=PerceptronTagger()
    def getName(self,word):
        # print chardet.detect(word)
        # print "word:"+word
        type = self.get_wordnet_pos(nltk.tag._pos_tag([word],None,self.tagger)[0][1])

        lemma = self.lmtzr.lemmatize(word, pos=type)
        lemma = lemma.encode("ascii")
        # print lemma
        # print chardet.detect(lemma)
        return lemma

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag[0] == 'J':
            return wordnet.ADJ
        elif treebank_tag[0] == 'V':
            return wordnet.VERB
        elif treebank_tag[0] == 'N':
            return wordnet.NOUN
        elif treebank_tag[0] == 'R':
            return wordnet.ADV
        else:
            return wordnet.NOUN
