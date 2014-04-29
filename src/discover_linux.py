import subprocess
import sqlite3 as sqlite

MAX_PROCESSES = 20 #Too many is a big preformance burden on the computer.

#Creates a list of all CS linux computers, tupled with their room
computers = []
def get_computers():
	c = []
	#Lawson
	c.extend(("SAC%02d" % i, "SAC", "LWSN B131")   for i in range(1,14)) 
	c.extend(("MOORE%02d" % i, "MOORE", "LWSN B146") for i in range(0,25))
	c.extend(("SSLAB%02d" % i, "SSLAB", "LWSN B158") for i in range(0,25)) 
	
	#POD Lab
	c.append(("POD0-0", "POD", "LWSN B148"))
	c.extend(("POD1-%d" % i, "POD", "LWSN B148") for i in range(1,6))
	c.extend(("POD2-%d" % i, "POD", "LWSN B148") for i in range(1,6))
	c.extend(("POD3-%d" % i, "POD", "LWSN B148") for i in range(1,6))
	c.extend(("POD4-%d" % i, "POD", "LWSN B148") for i in range(1,6))
	c.extend(("POD5-%d" % i, "POD", "LWSN B148") for i in range(1,6))
	
	#HAAS
	c.extend(("BORG%02d" % i, "BORG", "HAAS G40") for i in range(0,25))
	c.extend(("XINU%02d" % i, "XINU", "HAAS 257") for i in range(0,22))
	
	#MC01-MC18 are servers
	return c

#Starts who command on remote host
def start_subprocess(host):
  ssh = subprocess.Popen(['ssh', '%s' % host, 'who'], shell=False, 		
  												stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh
	

def build():
	notComplete = list(computers);
	processes = []
	completed = []
	
	#Spawn and track processes
	while notComplete or processes:
		while len(processes) < MAX_PROCESSES and len(notComplete) > 0:
			c = notComplete.pop()
			processes.append((c, start_subprocess(c[0])))
		
		for p in processes:
			if(p[1].poll() is not None):
				completed.append(p)
				processes.remove(p)

  
  #Build list
	lookup = []
	for p in completed:
		out = p[1].stdout.readlines()
		
		logged = False
		inuse = False
		for line in out:
			split = line.split()
			#comp name: p[0][0]
			#room			: p[0][1]
			#username : split[0]
			#tty 			: split[1] 
			
			logged = True
			inuse = "tty" in split[1]
			username = split[0]
			if inuse:
				#Otherwise, list order may have false positives on emptiness
				break
		
		#Were trying to avoid adding usernames to remoted in users
		lookup.append(( p[0][0], p[0][1], p[0][2], 
						int(inuse), username if inuse else ''))	
						
	
	return lookup
		
	
def execute(db_name):
	computer = build()
	
	connection = sqlite.connect(db_name)
	c = connection.cursor()
	
	c.executemany("INSERT OR REPLACE INTO computers VALUES (?,?,?,?,?)", computer);
	
	connection.commit()
	connection.close()

computers = get_computers()
