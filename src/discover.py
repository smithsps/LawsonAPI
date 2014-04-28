import subprocess
import User
import sqlite3 as sqlite
import logging
import os.path

DB_NAME = "discover.db"

#Builds the (new) sqlite3 database.
def build_db(){
    connection = sqlite.connect(DB_NAME)
    c = connection.cursor()
    
    
    c.execute('''CREATE TABLE computers (
        				name TEXT, 
        				lab TEXT,
        				room TEXT,
        				useable INTEGER,
        				user TEXT);''')
        				
    c.execute('''CREATE TABLE translation (
        				);''')
        
    connection.commit();
    connection.close();
}




if (!os.path.isfile(DB_NAME)):
	build_db();

	
