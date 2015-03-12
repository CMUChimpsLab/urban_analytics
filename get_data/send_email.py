#!/usr/bin/env python

# Dumb little file that has one function that sends me an email.
# (me b/c my name is in my config.txt.) Thanks to Hong Bin and Jennifer for
# figuring out how to do this!
import smtplib, ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.txt')
FROM_EMAIL = config.get('error_handling', 'email')
TO_EMAILS = config.get('error_handling_to_addr', 'email').split(',')
PSWD = config.get('error_handling', 'password')

def send_dan_email(subj, text):
    s = smtplib.SMTP('smtp.gmail.com', 587)  
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(FROM_EMAIL, PSWD)

    headers = ["from: " + FROM_EMAIL,
               "subject: " + subj,
               "to: " + ', '.join(TO_EMAILS),
               "mime-version: 1.0",
               "content-type: text/html"]
    headers = "\r\n".join(headers)
    body = text + "\r\n\r\n"

    s.sendmail(FROM_EMAIL, TO_EMAILS, headers + "\r\n\r\n" + body)
    s.quit()
    return

if __name__=='__main__':
    send_dan_email('test subject', 'test text')
