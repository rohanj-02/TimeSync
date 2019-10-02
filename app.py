from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from flask import *
import requests
import sqlite3
dic ={ }


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
conn = sqlite3.connect('data.db')
c = conn.cursor()
app = Flask(__name__)
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS courses (  name varchar[35], coursecode  varchar[35] , batch int  )")
    # conn.commit()

def data_entry():
    c.execute("INSERT INTO courses VALUES('INTRODUCTION TO PROGRAMMING A','CSE101 A',2019)")
    c.execute("INSERT INTO courses VALUES('DIGITAL CIRCUITS A','ECE111 A',2019)")
    c.execute("INSERT INTO courses VALUES('MATHS I A','MTH100 A',2019)")
    c.execute("INSERT INTO courses VALUES('INTRODUCTION TO PROGRAMMING B','CSE101 B',2019)")
    c.execute("INSERT INTO courses VALUES('DIGITAL CIRCUITS B','ECE111 B',2019)")
    c.execute("INSERT INTO courses VALUES('MATHS I B','MTH100 B',2019)")
    c.execute("INSERT INTO courses VALUES('PROTOTYPING INTERACTIVE SYSTEMS','PIS',2019)")

   
def read_from_db():
    
    c.execute('SELECT * FROM  student where name ="ROHAN JAIN" ')
    data = c.fetchall()
    for row in data:
        pr={'id':row[0],'name':row[1],'branch':row[2],'batch':row[3], 'courses':[{'coursecode': 'ECE111','starttime':'13:00:00','endtime':'14:00:00'},{'coursecode': 'MTH100','starttime':'17:00:00','endtime':'19:00:00'}]}
    return pr


create_table()
data_entry()
data = read_from_db()
c.close
conn.close()
@app.route('/')
def f1():
	return redirect('/login')

@app.route('/addEvent')
def f2():
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'creds.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('calendar', 'v3', credentials=creds)
	GMT_OFF = '+05:30'
	# for i in range(2):
	repeat = str(dic['Reday'])
	repeat = repeat[:2]
	repeat = repeat.upper()
	start = str(dic['StartTime'])
	start = start +":00"
	end =  str(dic['EndTime'])
	end = end + ":00"

	EVENT = {
		'summary':dic['name'],
		'start':{'dateTime':'2019-10-15T'+start+'%s'%GMT_OFF},
		'end':{'dateTime':'2019-10-15T'+end+'%s'%GMT_OFF},
		# 'recurrence' : [
		# 'RRULE:FREQ=WEEKLY;COUNT=50;BYDAY='+repeat],
		}
	e = service.events().insert(calendarId='primary',sendNotifications=True, body=EVENT).execute()
	return redirect('/success')


@app.route('/intermediate', methods = ['POST'])
def f3():
	username = request.form["username"]
	password = request.form["Password"]
	if username == "admin" and password == "admin":
		return redirect("/addCourse")
	else:
		return redirect("/login")

@app.route('/login')
def f4():
	return render_template("/login.html")

@app.route('/addCourse')
def f5():
	return render_template("/addCourse.html")

@app.route('/success')
def f6():
	return render_template('/success.html')

@app.route('/inter2',methods = ['POST'])
def f7():
	# //store data code
	Name=request.form['Name']
	CourseCode = request.form['Code']
	StartTime = request.form['TimeS']
	EndTime = request.form['TimeE']
	ReDay = request.form['Day']
	global dic
	dic={'name':Name,'course':CourseCode , 'StartTime':StartTime, 'EndTime':EndTime ,'Reday':ReDay}
	return redirect('/addCourse')

@app.route('/about')
def f8():
	return render_template('/about.html')


if __name__=="__main__":
	app.run(debug=True);

