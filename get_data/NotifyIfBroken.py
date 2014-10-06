import smtplib

from pymongo import MongoClient
client = MongoClient()
db = client.tweet
tweet_pgh = db.tweet_pgh
tweet_pgh_count = tweet_pgh.count()

with open('tweet_pgh_count', 'r') as f:
	prev = f.read()


if prev and int(prev)>= tweet_pgh_count:
	s = smtplib.SMTP('smtp.gmail.com', 587)
	
	s.ehlo()
	s.starttls()
	s.ehlo
	s.login('cmu.urbananalytics@gmail.com', 'chimpslab')
	


	headers = ["from: " + "cmu.urbananalytics@gmail.com",
           "subject: Error: stopped collecting tweet data",
           "to: " + "cmu.urbananalytics@gmail.com",
           "mime-version: 1.0",
           "content-type: text/html"]
	headers = "\r\n".join(headers)
	body = "Data collection stopped working"
	s.sendmail("cmu.urbananalytics@gmail.com", "cmu.urbananalytics@gmail.com",headers + "\r\n\r\n" + body)
	s.quit()



with open('tweet_pgh_count', 'w') as f:
	f.write(str(tweet_pgh_count))



