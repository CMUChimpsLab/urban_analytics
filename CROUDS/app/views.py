#!/usr/bin/env python

from dateutil import tz
from geopy.distance import vincenty
from flask import render_template
from app import app
from flask import abort, redirect, url_for, flash, Flask, request
from twython import Twython, TwythonStreamer
import json, requests, humanize, string, psycopg2, pytz, copy
from datetime import datetime, timedelta
from FindUsers import *
from GetQuestions import *
from AddQuestion import * 
from GetResponses import *

# To connect to Twitter Stream using OAuth 1
APP_KEY = 'GLIC9scXNOCQPMvW2Z3vDR0gP'
APP_SECRET = 'r4pxcSzlCyaHiTR5QFSpN20nLn24XXV06YL8gtxGUzc4wXhgLA'
ACCESS_TOKEN = '2875905140-02P20c7dHFDgb9yIE2jEqdlidS9xOGkdVq4nrGB'
ACCESS_TOKEN_SECRET = '42azhlc7p4Hi949NvPth3FmdJ8bZafzGqLIrAHKTXDOSi'

APP_KEY = 'UmLjRKeW4Gc9RlLUBqoNfpmyG'
APP_SECRET = 'qFCKEMZbLD7NO4ki2ksbibQ01SV88ECJQLZn3TQmQXiJkvN877'
ACCESS_TOKEN = '3307752328-R52HmpgczQt5tl8hYohaXZ9j0moNMOfAemNEdd1'
ACCESS_TOKEN_SECRET = 'eJNVo321y9Ancj08oJOo9Ii4KFHJIJgbyFSgaRuMGHb3x'


class UserSearch:
    def __init__(self):
        self.minutes = None
        self.home = None
        self.location = None
        self.location_type = None
        self.max_distance = None
        self.search_result = []

    def reset(self):
        self.minutes = None
        self.home = None
        self.location = None
        self.location_type = None
        self.max_distance = None
        self.search_result = []

class NewQuestion:
    def __init__(self):
        self.minutes = None
        self.home = None
        self.location = None
        self.location_type = None
        self.open_at = None
        self.close_at = None 

    def reset(self):
        self.minutes = None
        self.home = None
        self.location = None
        self.location_type = None
        self.open_at = None
        self.close_at = None 

twitter = Twython(APP_KEY, APP_SECRET,
                  ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# twitter.verify_credentials()
search = UserSearch()
new_question = NewQuestion()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/view_questions')
def view_questions():
    open_questions = GetQuestions.get_open_questions()
    return render_template('view_questions.html', open_questions= open_questions)

@app.route('/new_question')
def new_question():
    return render_template('new_question.html')

@app.route('/responses')
@app.route('/responses_parsed')
@app.route('/responses_unparsed')
def responses():
    responses = GetResponses.get_responses()
    return render_template("responses_parsed.html", responses= responses)

@app.route('/template')
def template():
    return render_template('responses_template.html') 

@app.route('/users')
def users():
    result = search.search_result
    count = len(result)
    return render_template('users.html',users=result, count=count) 


@app.route('/search_users')
def search_users():
    result = search.search_result
    count = len(result)
    return render_template('search_users.html',users=result, count=count) 

@app.route('/enqueue_question', methods=['POST'])  ###
def enqueue_question():
    new_question = NewQuestion()
    new_question.subject = str(request.form['subject'])
    new_question.question = str(request.form['question'])
    new_question.open_at = open_at = str(request.form['open_at']) # '2000-01-01T05:00'
    new_question.close_at = close_at = str(request.form['close_at'])

    if request.form['location'] == 'venue-name':
        new_question.location = 'venue name'
        new_question.location = str(request.form['venue-name'])
    elif request.form['location'] == 'venue-id': 
        new_question.location = 'venue id'
        new_question.location= str(request.form['venue-id'])

    elif request.form['location'] == 'streets': 
        new_question.location = 'streets'
        street_1, street_2 = str(request.form['venue-street-1']), str(request.form['venue-street-2'])
        new_question.location = street_1 + '&' + street_2

    open_at = datetime.strptime(open_at, '%Y-%m-%dT%H:%M') 
    close_at = datetime.strptime(close_at, '%Y-%m-%dT%H:%M')
    delta = timedelta(minutes=5)
    send_times = new_question.send_times = perdelta(open_at, close_at, delta) 
    AddQuestion.add(new_question) # add question to db
    return redirect(url_for('view_questions'))

@app.route('/query_users', methods=['POST']) 
def query_users():
    search.reset()
    search.home = str(request.form['home'])
    search.minutes = str(request.form['minutes'])
    search.location_type = str(request.form['location_type']) 
    search.max_distance = int(request.form['max_distance'])

    if (search.location_type == 'venue name' 
        or search.location_type == 'venue id'): 
        search.location = str(request.form['venue'])
    elif (search.location_type == 'streets'):
        search.location = [str(request.form['street-1']), str(request.form['street-2'])]
    else: # user's location not specified
        search.location_type = None
        search.location = None

    if search.home == 'Any':    
        search.home = None

    search.search_result = FindUsers.search(  
                minutes_since = search.minutes,
                home = search.home,
                location_type = search.location_type,
                location = search.location,
                max_distance = search.max_distance)

    return redirect(url_for('users'))

# Helper Fn's
def perdelta(start, end, delta):
    times = []
    timestamp = start
    while timestamp < end:
        times.append(timestamp)
        timestamp += delta
    return times

