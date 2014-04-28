import subprocess
import sqlite3 as sqlite
import logging
import os.path
import discover_linux
import discover_windows
import discover_users

DB_NAME = "discover.db"

#Builds the a new sqlite3 database, if missing.
def build_db():
		if (not os.path.isfile(DB_NAME)):
		  connection = sqlite.connect(DB_NAME)
		  c = connection.cursor()
		  
		  #name, lab, room, useable, user
		  c.execute('''CREATE TABLE computers (
		      				name TEXT PRIMARY KEY, 
		      				lab TEXT,
		      				room TEXT,
		      				useable INTEGER,
		      				user TEXT)''')
		  
		  #username, name
		  c.execute('''CREATE TABLE users (
		      				username TEXT PRIMARY KEY,
		      				name TEXT)''')
		      
		  connection.commit();
		  connection.close();


def print_db():
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	print "Computers:"
	for row in c.execute("SELECT * FROM computers"):
		print row
		
	#print "\nUsernames:"
	#for row in c.execute("SELECT * FROM translation"):
		#print row
	
	connection.close();


def test():
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	c.execute("INSERT OR REPLACE INTO computers VALUES ('tst01', 'SAC', 'B134', 1, 'smithsp')")
	connection.commit()
	connection.close()
	
	print_db()
	
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	c.execute("DELETE FROM computers WHERE name='tst01'")
	connection.commit()
	connection.close()
	
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	c.execute("SELECT * FROM users WHERE username='smithsp'")
	print c.fetchone()[1]

build_db();
discover_users.execute(DB_NAME)

test();
