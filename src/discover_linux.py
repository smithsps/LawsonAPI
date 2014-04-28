import subprocess

#Creates a list of all CS linux computers, tupled with their room
computers = []
def get_computers():
	c = []
	#Lawson
	c.extend(("SAC%02d" % i, "LWSN B131")   for i in range(1,14)) #SAC LAB
	c.extend(("MOORE%02d" % i, "LWSN B146") for i in range(0,25)) #MOORE LAB
	c.extend(("SSLAB%02d" % i, "LWSN B158") for i in range(0,25)) #SSLAB LAB
	
	#POD Lab
	c.append(("POD0-0", "LWSN B148"))
	c.extend(("POD1-%d" % i, "LWSN B148") for i in range(1,6))
	c.extend(("POD2-%d" % i, "LWSN B148") for i in range(1,6))
	c.extend(("POD3-%d" % i, "LWSN B148") for i in range(1,6))
	c.extend(("POD4-%d" % i, "LWSN B148") for i in range(1,6))
	c.extend(("POD5-%d" % i, "LWSN B148") for i in range(1,6))
	
	
	#HAAS
	c.extend(("BORG%02d" % i, "HAAS G40") for i in range(0,25)) #BORG LAB
	c.extend(("XINU%02d" % i, "HAAS 257") for i in range(0,22)) #Xinu Lab
	
	#MC01-MC18 are servers
	
	return c

#Starts who command on remote host
def who(host):
  ssh = subprocess.Popen(['ssh', '%s' % host, 'who'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh
	

def build():
	pass


def execute():
	pass

computers = get_computers()
for v in computers:
	print v
