import sqlite3 as sqlite
import simplejson as json
from bottle import Bottle, error, static_file, run

DB_NAME = "discover.db"

app = Bottle()

@app.route('/lab/<name>')
def lab(name):
	return "Specfic Lab: " + name

@app.route('/labs')
def labs():
	j = {"labs" : []}
	
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	
	c.execute("SELECT * FROM labs ORDER BY name")
	labs = c.fetchall()
	for row in labs:
		build = {"name" : row[0]}
		build["room"] = row[1]
		build["event"] = { "ongoing" : row[2], "time" : row[3], "name" : row[4] }
		build["status"] = row[5]
		total = 0
		inuse = 0
		for crow in c.execute("SELECT * FROM computers WHERE lab='" + build["name"] +"'"):
			if crow[4] != 0:
				inuse += 1
			total += 1
		build["people"] = { "current" : inuse, "capacity" : total }
		j["labs"].append(build)
	
	return json.dumps(j, sort_keys=True)
		

@app.route('/computer/<name>')
def computer(name):
	return "One computer: " + name	
	
@app.route('/computers')
def computers():
	return "All computers"

@app.route('/computers/lab/<name>')
def labcomputers(name):
	return "All computers of " + name
	
@error(404)
@app.route('/')
def index():
	return static_file("index.html", root="www/")
	
run(app, host='sslab13.cs.purdue.edu', port=8000, debug=True)
