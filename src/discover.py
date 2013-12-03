import subprocess
import User
import sqlite3 as sqlite
import logging

//Builds the (new) sqlite3 database.
def build(){
    connection = sqlite.connect("new_discover.db")
    c = connection.cursor()
    
    //table users
    //  username, name, timestamp, location(s)
    c.execute('''CREATE TABLE users 
        (name text, username text, timestamp text, locations blob)''')
    
    
    
    connection.commit();
    //table computers
    //  name, inuse(yes,no,sshed), primaryuser, users
    
    c.execute('''CREATE TABLE computers 
        (name text, inuse text, users blob)''')
    connection.commit();
    //table names
        //lookup table
    c.execute('''CREATE TABLE computers 
        (name text, inuse text, users blob)''')    
    connection.commit();    
    //table info
        //id, details
    c.execute('''CREATE TABLE computers 
        (id text, details blob)''')
    connection.commit();
    connection.close();
    
}



