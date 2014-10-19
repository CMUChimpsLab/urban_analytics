# Emails us if we haven't received any Tweets, Instagrams, or Flickrs in a day.
# Email addresses (from and to) given in config.txt.

import smtplib
import json
import ConfigParser
from pymongo import MongoClient

config = ConfigParser.ConfigParser()
config.read('config.txt')

FROM_EMAIL = config.get('error_handling', 'email')
TO_EMAILS = config.get('error_handling_to_addr', 'email').split(',')
PSWD = config.get('error_handling', 'password')

COUNT_FILENAME = 'data_counts'


def email_error(data_name, prev_count, current_count):
    s = smtplib.SMTP('smtp.gmail.com', 587)  
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(FROM_EMAIL, PSWD)

    headers = ["from: " + FROM_EMAIL,
               "subject: Error: stopped collecting " + data_name + " data",
               "to: " + ', '.join(TO_EMAILS),
               "mime-version: 1.0",
               "content-type: text/html"]
    headers = "\r\n".join(headers)
    body = "Data collection seems to be not working. \r\n\r\n" \
           + "Data: " + data_name + "\r\n\r\n" \
           + "Previous count: " + str(prev_count) + "\r\n\r\n" \
           + "Current count: " + str(current_count)

    s.sendmail(FROM_EMAIL, TO_EMAILS, headers + "\r\n\r\n" + body)
    s.quit()
    return

def data_not_updated(data_name):
    return prev_counts.get(data_name) \
        and current_counts.get(data_name) \
        and prev_counts.get(data_name) >= current_counts.get(data_name)

if __name__ == '__main__':

    client = MongoClient()
    tweet_db = client.tweet
    flickr_db = client.flickr
    instagram_db = client.instagram

    instagram_count = instagram_db.instagram_pgh.count()
    flickr_count = flickr_db.flickr_pgh.count()
    tweet_pgh_count = tweet_db.tweet_pgh.count()
    tweet_sf_count = tweet_db.tweet_sf.count()

    current_counts = {'tweet_pgh_count': tweet_pgh_count, 
                      'tweet_sf_count': tweet_sf_count, 
                      'flickr_count': flickr_count,
                      'instagram_count': instagram_count}

    # if file does not exist, make one.
    try:
        f = open(COUNT_FILENAME, 'r')
        prev_counts = json.load(f)
        f.close()
    except:
        prev_counts = {'tweet_pgh_count': 0, 
                       'tweet_sf_count': 0, 
                       'flickr_count': 0,
                       'instagram_count': 0}
        f = open(COUNT_FILENAME, 'w')
        f.write(json.dumps(prev_counts))
        f.close()

    if data_not_updated('tweet_pgh_count'):
        email_error('tweet_pgh', prev_counts['tweet_pgh_count'], current_counts['tweet_pgh_count'])
    if data_not_updated('tweet_sf_count'):
        email_error('tweet_sf', prev_counts['tweet_sf_count'], current_counts['tweet_sf_count'])
        del current_counts['tweet_sf_count']
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
