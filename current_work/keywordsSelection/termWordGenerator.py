import dbProcess, os, copy
tbname='tweet_pgh_ttt'
dbname='Neeraj'
user='postgres'
pg=dbProcess.PgController(tbname,dbname,user)


output = open('termWord.txt', 'w')
pg.cur.execute('''
	select id,senti_val,lon,lat,txt,term
	from %s where auto_tweet is Null;'''%pg.tbname)
for (id,senti_val,lon,lat,txt,term) in pg.cur.fetchall():
    term = term.split(",")
    for i in range(0,len(term)):
        output.write("%s "%term[i])
    output.write("\n")
output.close()