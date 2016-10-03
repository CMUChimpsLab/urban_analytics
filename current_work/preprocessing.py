"""
Preprocessing text and html (Tokenizing words and sentences, clean HTML, clean text, removing stopwords, stemming and lemmatization)
__author__ : Triskelion user@Kaggle (Thanks: Abhishek Thakur & Foxtrot user@Kaggle)
"""

# -*- coding: utf-8 -*-

from nltk import clean_html
from nltk import SnowballStemmer
from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re
import getCorrectName

# Tokenizing (Document to list of sentences. Sentence to list of words.)
textFormulate = getCorrectName.GetCorrectName()
textmapp = {}
def tokenize(str):
	'''Tokenizes into sentences, then strips punctuation/abbr, converts to lowercase and tokenizes words'''
	return 	[word_tokenize(" ".join(re.findall(r'\w+', t,flags = re.UNICODE | re.LOCALE)).lower()) 
			for t in sent_tokenize(str.replace("'", ""))]

def tokenize_tweet(str):
	#revised tokenize, fit tweet tokenization
	t=str.replace("'", "")
	return word_tokenize(" ".join(re.findall(r'\w+', t,flags = re.UNICODE | re.LOCALE)).lower())

#Removing stopwords. Takes list of words, outputs list of words.
def remove_stopwords(l_words, lang='english'):
	l_stopwords = stopwords.words(lang)
	content = [w for w in l_words if w.lower() not in l_stopwords]
	return content

def unify_format(l_words, lang='english'):
	for i in range(len(l_words)):
		if l_words[i] not in textmapp:
			textmapp[l_words[i]] = textFormulate.getName(l_words[i])
		l_words[i] = textmapp[l_words[i]]
	return l_words
		
#Clean HTML / strip tags TODO: remove page boilerplate (find main content), support email, pdf(?)
def html2text(str):
	return clean_html(str)
		
#Stem all words with stemmer of type, return encoded as "encoding"
def stemming(words_l, type="PorterStemmer", lang="english", encoding="utf8"):
	supported_stemmers = ["PorterStemmer","SnowballStemmer","LancasterStemmer","WordNetLemmatizer"]
	if type is False or type not in supported_stemmers:
		return words_l
	else:
		l = []
		if type == "PorterStemmer":
			stemmer = PorterStemmer()
			for word in words_l:
				l.append(stemmer.stem(word).encode(encoding))
		if type == "SnowballStemmer":
			stemmer = SnowballStemmer(lang)
			for word in words_l:
				l.append(stemmer.stem(word).encode(encoding))
		if type == "LancasterStemmer":
			stemmer = LancasterStemmer()
			for word in words_l:
				l.append(stemmer.stem(word).encode(encoding))
		if type == "WordNetLemmatizer": #TODO: context
			wnl = WordNetLemmatizer()
			for word in words_l:
				l.append(wnl.lemmatize(word).encode(encoding))
		return l

#The preprocess pipeline. Returns as lists of tokens or as string. If stemmer_type = False or not supported then no stemming.		
def preprocess_pipeline(str, lang="english", stemmer_type="PorterStemmer", return_as_str=False, 
						do_remove_stopwords=False, do_clean_html=False):
	l = []
	words = []
	if do_clean_html:
		sentences = tokenize(html2text(str))
	else:
		sentences = tokenize(str)
	for sentence in sentences:
		if do_remove_stopwords:
			words = remove_stopwords(sentence, lang)
		else:
			words = sentence
		words = stemming(words, stemmer_type)
		if return_as_str:
			l.append(" ".join(words))
		else:
			l.append(words)
	if return_as_str:
		return " ".join(l)
	else:
		return l

#test_sentence = "User-Testing Tester Tests! She had me at 'hello'?!? But then <abbr>ESPN</abbr> fainted... and Eighty cars drove past."
#print "\nOriginal:\n", test_sentence
#print "\nPorter:\n", preprocess_pipeline(test_sentence, "english", "PorterStemmer", True, False, True)
#print "\nLancaster:\n", preprocess_pipeline(test_sentence, "english", "LancasterStemmer", True, False, True)
#print "\nWordNet:\n", preprocess_pipeline(test_sentence, "english", "WordNetLemmatizer", True, False, True)
#print "\nStopword Tokenized Lancaster:\n", preprocess_pipeline(test_sentence, "english", "LancasterStemmer", False, True, True)
#print "\nOnly cleaning (HTML+Text):\n", preprocess_pipeline(test_sentence, "english", False, True, False, True)