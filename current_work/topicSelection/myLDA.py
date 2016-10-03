import dbProcess, os, copy
import logging
from gensim import corpora, models, similarities
import gc


tbname='tweet_pgh_ttt'
dbname='Neeraj'
user='postgres'
pg=dbProcess.PgController(tbname,dbname,user)

# for i in range(7):
#     topic[i] = pre.stemming(topic[i])

senti_val_sum = [ [ 0 for i in range(7) ] for j in range(18) ]
senti_val_count = [ [ 0 for i in range(7) ] for j in range(18) ]
texts = []
pg.cur.execute('''
	select id,senti_val,lon,lat,txt,term
	from %s where auto_tweet is Null limit 100000;'''%pg.tbname)
for (id,senti_val,lon,lat,txt,term) in pg.cur.fetchall():
	term = term.split(",")
	texts.append(term)
print "reading finished"
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]
dictionary = corpora.Dictionary(texts)
# dictionary.save('./tmp/deerwester.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
del texts
gc.collect()
print "preprocessing finished"
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=5)


myresult = lda.print_topics(100)
words = {}
outfd = open("ldaResult.txt","w")
for iteri in myresult:
	outfd.write('%s %s\n'%iteri)
outfd.close()