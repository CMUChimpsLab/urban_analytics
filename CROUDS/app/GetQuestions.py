#!/usr/bin/python

import psycopg2

class GetQuestions():

    @staticmethod
    def get_open_questions():
        print 'getting questions'
        conn = psycopg2.connect(database="tweet", user="jinnyhyunjikim")
        cur = conn.cursor()
        statement = """SELECT question_id, question, location, subject,
        start_time, end_time, users_sent
        FROM question WHERE end_time > now() ORDER BY question_id DESC ; """
        statement = """SELECT question_id, question, location, start_time
        FROM question WHERE end_time > now() ORDER BY question_id DESC ; """
        statement = """SELECT question_id, question, subject, location, start_time, end_time, send_times
        FROM question ORDER BY question_id DESC ; """
        cur.execute(statement)
        open_questions = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        open_questions_list = [] # insert  dictionary here
        columns = ('question_id', 'question', 'subject', 'location', 
            'start_time', 'end_time', 'send_times') 
        for question in open_questions:
            open_questions_list.append(dict(zip (columns, question)))

        return open_questions_list

    @staticmethod
    def get_closed_questions():
        return []