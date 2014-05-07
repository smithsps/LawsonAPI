import sqlite3 as sqlite
import time
from datetime import timedelta, datetime
import requests

calendar_default_url = "https://www.googleapis.com/calendar/v3/calendars/"
calendar_key = "AIzaSyB1u9HeHTK-wO2H3uozwwJSct2I1cpURL4" #We'll cross this bridge when we meet it.

#2014-05-07 03:00:56.894544 Our datetime.tostring
#2014-05-07T03:00:56-04:00	Google Time Lords
def build_google_time(dt):
	t = str(dt)
	spl = t.split(" ")
	doublespl = spl[1].split(".")
	
	#This is pretty hackish, someone should *definitely* eventually maybe fix this.
	return spl[0] + "T" + doublespl[0] + "-04:00"

class Lab:
	name = ""
	calendar_id = ""
	
	event = False
	eventTime = ""
	eventName = ""
	
	eventStart = ""
	eventEnd = ""
	
	status = ""
	def __init__(self, name, calendar_id):
		self.name = name
		self.calendar_id = calendar_id

def build_lablist():
	return [Lab("SAC", "isp5jp397bj8et0i5r8g6kd3uo@group.calendar.google.com"),
			 Lab("MOORE", "1r5tgrb2sln4oe4h4f4gfeece8@group.calendar.google.com"),
			 Lab("POD", "hd9ldosmo9upm7u5scvq8uumig@group.calendar.google.com"),
			 Lab("SSLAB", "25m91hh3dpdlcguv5h30i749pg@group.calendar.google.com"),
			 Lab("K9", "bvh903t70gtpvgtl6m8vhl2e1s@group.calendar.google.com"),
			 Lab("BORG", "jv11mjte5oupheck2kmv36mn2o@group.calendar.google.com"),
			 Lab("XINU", "tg56f4t31msvg4o56iuf37luqk@group.calendar.google.com")]
			 


def build():
	now = datetime.now()+timedelta(0.4, 0)
	google_max = build_google_time(now)
	slightlybeforenow = now - timedelta(0,1)
	google_min = build_google_time(slightlybeforenow);
	
	payload = {'maxResults' : '1', 'orderBy' : 'startTime', 'singleEvents' : 'true',
							 'timeMax' : google_max, 'timeMin' : google_min, 'key' : calendar_key} 
	
	for lab in labs:
		r = requests.get(calendar_default_url + lab.calendar_id + "/events", params=payload)

		json = r.json()
		for item in json["items"]:
			lab.eventName = item["summary"]
			lab.eventStart = item["start"]
			lab.eventEnd = item["end"]
			lab.event = True
			lab.status = "Class In Session"
			
		if (not lab.event):
			if (now.hour in range(2, 6)):
				lab.status = "Room Locked"
	
	
	lookup = []
	for lab in labs:
		#Some date phrasing
		if lab.event:
			start = lab.eventStart["dateTime"].split("T")[1].split("-")[0]
			end = lab.eventEnd["dateTime"].split("T")[1].split("-")[0]
			lab.eventTime = start + " - " + end
			print lab.eventTime
			
		lookup.append((lab.name, int(lab.event), lab.eventTime, lab.eventName, lab.status))
	
	return lookup
	
def execute(db_name):
	lookup = build()
	
	connection = sqlite.connect(db_name)
	c = connection.cursor()
	
	c.executemany("INSERT OR REPLACE INTO labs VALUES (?,?,?,?,?)", lookup);
	
	connection.commit()
	connection.close()
	
	
labs = build_lablist()


