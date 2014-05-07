class Computer(object):
	name = ""
	lab = ""
	room = ""
	os = ""
	inuse = False
	loggedIn = False
	error = False
	username = ""
	
	process = None
	processTime = None
	
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

