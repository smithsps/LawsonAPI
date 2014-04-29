import subprocess
import sqlite3 as sqlite
import time

MAX_PROCESSES = 30 #Too many is a big preformance burden on the computer.
PROCESS_TIMEOUT = 15 #Timeout for checking computer if unreachable

#Instead of using a complex tuple list, we'll just use an object list
class Computer(object):
	name = ""
	lab = ""
	room = ""
	inuse = False
	loggedIn = False
	username = ""
	
	process = None
	processTime = None
	failed = False
	
	def __init__(self, name, lab, room):
		self.name = name
		self.lab = lab
		self.room = room
	
	#Instead of calling many python generators we have this nice thing
	@staticmethod
	def many(lab, number, room, lower, upper):
		return (Computer(lab + number % i, lab, room) for i in range(lower, upper + 1))
		
	def __str__(self):
		return name + " : " + lab + " : " + room + " : " + inuse


#Creates a list of all CS linux computers, tupled with their room
computer_names = []
def get_computers():
	c = []
	#Lawson
	c.extend(Computer.many("SAC", "%02d", "LWSN B131", 1, 13))
	c.extend(Computer.many("MOORE", "%02d", "LWSN B146", 0, 24))
	c.extend(Computer.many("SSLAB", "%02d", "LWSN B158", 0, 24))
	
	#POD Lab
	c.append(Computer("POD0-0", "POD", "LWSN B148"))
	c.extend(Computer.many("POD", "1-%d", "LWSN B148", 1, 5))
	c.extend(Computer.many("POD", "2-%d", "LWSN B148", 1, 5))
	c.extend(Computer.many("POD", "3-%d", "LWSN B148", 1, 5))
	c.extend(Computer.many("POD", "4-%d", "LWSN B148", 1, 5))
	c.extend(Computer.many("POD", "5-%d", "LWSN B148", 1, 5))
	
	#HAAS
	c.extend(Computer.many("BORG", "%02d", "HAAS G40", 0, 24))
	c.extend(Computer.many("XINU", "%02d", "HAAS 257", 0, 21))
	
	#MC01-MC18 are servers
	return c

#Starts who command on remote host
def start_subprocess(host):
  ssh = subprocess.Popen(['ssh', '%s' % host, 'who'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh
	

def build():
	notStarted = computer_names;
	processes = []
	failed = []
	completed = []
	
	#Spawn and track processes
	while notStarted or processes:
		while len(processes) < MAX_PROCESSES and len(notStarted) > 0:
			c = notStarted.pop()
			c.process = start_subprocess(c.name)
			c.processTime = time.time()
			processes.append(c)
		
		#print len(processes)
		
		#Check if current processes are finished
		for c in processes:
			if(c.process.poll() is not None):
				completed.append(c)
				processes.remove(c)
			elif (time.time() - c.processTime) > PROCESS_TIMEOUT:
				c.failed = True
				failed.append(c)
				processes.remove(c)

				
		time.sleep(0.1)

  
  #Build sql list for query
	lookup = []
	for c in completed:
		out = c.process.stdout.readlines()
		
		for line in out:
			split = line.split()
			#username : split[0]
			#tty 			: split[1] 
			
			c.logged = True
			c.inuse = "tty" in split[1]
			if c.inuse: 
				c.username = split[0]
				break
		
		lookup.append(( c.name, c.lab, c.room, int(c.inuse), c.username))
	
	#Perhaps a status for the computer later. These computers are unreachable
	for c in failed:
		lookup.append(( c.name, c.lab, c.room, int(True), ""))
	
	return lookup
		
	
def execute(db_name):
	computer = build()
	
	connection = sqlite.connect(db_name)
	c = connection.cursor()
	
	c.executemany("INSERT OR REPLACE INTO computers VALUES (?,?,?,?,?)", computer);
	
	connection.commit()
	connection.close()

computer_names = get_computers()
