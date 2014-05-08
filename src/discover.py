import subprocess
import sqlite3 as sqlite
import logging
import os.path
import time
import getpass
import discover_linux
import discover_windows
import discover_users
import discover_labs

DB_NAME = "discover.db"

#Builds the a new sqlite3 database, if missing.
def build_db():
		if (not os.path.isfile(DB_NAME)):
			print "Building new SQLite database."
			connection = sqlite.connect(DB_NAME)
			c = connection.cursor()

			#name, lab, room, useable, user
			c.execute('''CREATE TABLE computers (
									name TEXT PRIMARY KEY, 
									lab TEXT,
									room TEXT,
									os TEXT,
									useable INTEGER,
									error INTEGER,
									user TEXT)''')

			#username, name
			c.execute('''CREATE TABLE users (
									username TEXT PRIMARY KEY,
									name TEXT)''')
								
			c.execute('''CREATE TABLE labs (
									name TEXT PRIMARY KEY,
									room TEXT,
									event INTEGER,
									eventTime TEXT,
									eventName TEXT,
									status TEXT)''')
								
			connection.commit();
			connection.close();


def print_db():
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	print "Computers:"
	for row in c.execute("SELECT * FROM computers ORDER BY name"):
		print row
		
	print "\nUsernames:"
	for row in c.execute("SELECT * FROM users ORDER BY name"):
		print row
		
	print "\nLabs:"
	for row in c.execute("SELECT * FROM labs"):
		print row
	
	connection.close();


def test():
	
	print_db()
	
	connection = sqlite.connect(DB_NAME)
	c = connection.cursor()
	c.execute("SELECT * FROM computers WHERE user='smithsp'")
	print c.fetchone()

def run():
	discover_users.execute(DB_NAME)
	discover_linux.execute(DB_NAME)
	discover_labs.execute(DB_NAME);

#user = getpass.getuser() 
#password = getpass.getpass("Enter password for " + user + " (USED FOR WINDOWS COMPUTERS):")
build_db()
while True:
	run()
	time.sleep(60)

#test();
