import smtplib
import json
import ConfigParser
from pymongo import MongoClient

config = ConfigParser.ConfigParser()
config.read('config.txt')

EMAIL = config.get('error_handling', 'email')
PSWD = config.get('error_handling', 'password')

COUNT_FILENAME = 'data_counts'

client = MongoClient()
db = client.tweet
instagram_count = db.instagram.count()
flickr_count = db.flickr.count()
tweet_pgh_count = db.tweet_pgh.count()

current_counts = {'tweet_pgh_count': tweet_pgh_count, 
                  'flickr_count': flickr_count,
                  'instagram_count': instagram_count}

# if file does not exist, make one.
try:
  f = open(COUNT_FILENAME, 'r')
  prev_counts = json.load(f)
  f.close()
except:
  prev_counts = {'tweet_pgh_count': 0, 
                  'flickr_count': 0,
                  'instagram_count': 0}
  f = open(COUNT_FILENAME, 'w')
  f.write(json.dumps(prev_counts))
  f.close()

def data_not_updated(data_name):
  return prev_counts.get(data_name) \
      and current_counts.get(data_name) \
      and prev_counts.get(data_name) >= current_counts.get(data_name)

def email_error(data_name, prev_count, current_count):
  s = smtplib.SMTP('smtp.gmail.com', 587)  
  s.ehlo()
  s.starttls()
  s.ehlo
  s.login(EMAIL, PSWD)

  headers = ["from: " + EMAIL,
             "subject: Error: stopped collecting " + data_name + " data",
             "to: " + EMAIL,
             "mime-version: 1.0",
             "content-type: text/html"]
  headers = "\r\n".join(headers)
  body = "Data collection seems to be not working. \r\n\r\n" \
         + "Data: " + data_name + "\r\n\r\n" \
         + "Previous count: " + str(prev_count) + "\r\n\r\n" \
         + "Current count: " + str(current_count)

  s.sendmail(EMAIL, EMAIL, headers + "\r\n\r\n" + body)
  s.quit()
  return

if data_not_updated('tweet_pgh_count'):
  email_error('tweet', prev_counts['tweet_pgh_count'], current_counts['tweet_pgh_count'])
  del current_counts['tweet_pgh_count']
if data_not_updated('instagram_count'):
  email_error('instagram', prev_counts['instagram_count'], current_counts['instagram_count'])
  del current_counts['instagram_count']
if data_not_updated('flickr_count'):
  email_error('flickr', prev_counts['flickr_count'], current_counts['flickr_count'])
  del current_counts['flickr_count']

with open(COUNT_FILENAME, 'w') as f:
  # update only the counts that increased
  for k in prev_counts:
    if k in current_counts:
      prev_counts[k] = current_counts[k]
  f.write(json.dumps(prev_counts))
