import subprocess
import sqlite3 as sqlite
import time
import discover
from Computer import Computer

computers = []
def get_computers():
	c = []
	#Lawson
	c.extend(Computer.many("K9", "%02d", "LWSN B160", 0, 25))
	#c.extend(Computer.many("HA", "%02d", "HAAS G56", 0, 24))
	
	#MC01-MC18 are servers
	return c
	
def start_subprocess(host):
	#	timeout 4 ./winexe-static -U "SERVERS\smithsp" --password "" //k9-00.cs.purdue.edu "cmd.exe" <<< "wmic /user:\"SERVERS\smithsp\" /password:\"humble54\" /node:\"k9-$i.cs.purdue.edu\" computersystem get username" >> test.txt
  ssh = subprocess.Popen(['ssh', '%s' % host, 'who'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh	
	
	
def build():
	

def execute():
	pass	
	
	
	
computers = get_computers()
