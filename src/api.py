import sqlite3 as sqlite
from bottle import route, run


@route('/')
def hello():
	return "Hello world!"
	
run(host='localhost', port=8000, debug=True)
