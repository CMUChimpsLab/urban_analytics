#!/usr/bin/python

import psycopg2, psycopg2.extras

class AddQuestion():

	@staticmethod
	def add(new_question):
		q_id = getNextRowID(tablename="question")
		subject, question = new_question.subject, new_question.question
		open_at, close_at = new_question.open_at, new_question.close_at
		send_times = new_question.send_times

		location_type =new_question.location_type
		location = new_question.location
		add_question_to_db(location_type, location, send_times, q_id, 
			subject, question, open_at, close_at)

def add_question_to_db(location_type, location, send_times, *data):
	conn = psycopg2.connect(database="tweet", user="jinnyhyunjikim")
	cur = conn.cursor()
	psycopg2.extras.register_hstore(conn)
	columns_question = ('(question_id, subject, question, start_time,\
end_time, send_times, location)')
	location_hstore = {'location type': location_type, 'location': location,}
	data = list(data)
	data = tuple(data) 
	values = str(data)
	values = values[:-1] + ', %s, %s)' # placeholder for location_hstore

	statement = "INSERT INTO question " + columns_question + " VALUES %s;" %(values) 
	cur.execute(statement, [send_times, location_hstore])
	conn.commit()
	cur.close()
	conn.close()

def getNextRowID(tablename):
	conn = psycopg2.connect("dbname=tweet user=jinnyhyunjikim")
	cur = conn.cursor()
	if tablename == 'question':
		query = "SELECT max(question_id) FROM question;"
	elif tablename == 'question_user':
		query = "SELECT max(user_id) FROM question_user;"
	else:
		print "No table named " + tablename + " in psql tweet database."
		return
	cur.execute(query)
	result = cur.fetchone()
	conn.commit()
	cur.close()
	conn.close()
	max_id = result[0]
	if max_id == None: # table empty
		return 0
	return max_id + 1

