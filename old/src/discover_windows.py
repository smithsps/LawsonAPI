import subprocess
import sqlite3 as sqlite
import time
from Computer import Computer

computers = []
def get_computers():
	c = []
	#Lawson
	c.extend(Computer.many("K9", "%02d", "LWSN B160", 0, 25))
	#c.extend(Computer.many("HA", "%02d", "HAAS G56", 0, 24))
	
	#MC01-MC18 are servers
	return c
	
def start_subprocess(host, user, password):
	#	timeout 4 ./winexe-static -U "SERVERS\smithsp" --password "" //k9-00.cs.purdue.edu "cmd.exe" <<< "wmic /user:\"SERVERS\smithsp\" /password:\"humble54\" /node:\"k9-$i.cs.purdue.edu\" computersystem get username" >> test.txt
  arguments = ["timeout", "2", "./winexe-static", "-U", 
  						 "SERVERS\\" + user, 
  						 "--password", "" + password + "", 
  						 "//k9-00.cs.purdue.edu", "\"cmd.exe\""]
  
  wmic_command = "wmic /user:\"SERVERS\\" + user + "\" /password:\"" + password + "\" /node:\"" + host + ".cs.purdue.edu\" computersystem get username"
  	
  ssh = subprocess.Popen(arguments, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  
  #wmic_stdout = ssh.communicate(input=wmic_command)
  
  print arguments
  print wmic_command
  
  return ssh
	
	
def build(user, password):
	print start_subprocess("K9-00", user, password);	

def execute(db_name, user, password):
	build(user, password)	
	

	
computers = get_computers()
