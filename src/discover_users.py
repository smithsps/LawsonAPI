import subprocess
import sqlite3 as sqlite

#Builds a list of all users from /etc/passwd on lore.
def build():
  ssh = subprocess.Popen(['ssh', 'lore', 'cat', '/etc/passwd'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  raw = ssh.stdout.readlines()
  
  lookup = []
  for line in raw:
    rawSplit = line.split(":")
    lookup.append((rawSplit[0], rawSplit[4].strip(',')))

  return lookup


def execute(db_name):
	users = build()
	connection = sqlite.connect(db_name)
	c = connection.cursor()
	
	c.executemany("INSERT OR REPLACE INTO users VALUES (?,?)", users);
	
	connection.commit()
	connection.close()
