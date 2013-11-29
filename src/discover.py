import subprocess
import User


# Starts ssh process an and returns it
#NOT USED ATM
def ssh(host, command):
  #https://gist.github.com/bortzmeyer/1284249
  ssh = subprocess.Popen(['ssh', '%s' % host,  '%s' % command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh

#Runs who command with ssh return subprocess
def who(host):
  ssh = subprocess.Popen(['ssh', '%s' % host, 'who'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh
  #who = ssh.stdout.readlines()
  
  '''users = list()
  for line in who:
    split = line.split();
    #print(split[1])
    users.append(User.User(split[0], identify(split[0]), ' '.join(split[2:5]), split[1] + '-' + host))
  return ssh
  '''
def who_list(hosts):
  processes = list()
  for host in hosts:
    # [ name, process]
    processes.append([host, who(host)])

  return processes

#Go to Lore and get /etc/passwd
#Put into dictionary, return
def getLookupTable():
  ssh = subprocess.Popen(['ssh', 'lore', 'cat', '/etc/passwd'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  raw = ssh.stdout.readlines()
  
  #Get Usernames:Names add to dictionary
  lookup = dict()
  for line in raw:
    rawSplit = line.split(":")
    lookup[rawSplit[0]] = rawSplit[4].strip(',')
  
  #print(lookup)

  return lookup
  
def identify(username):
  #TODO use static lookuptable if advailable
  if(not identify.lookup):
    print("Getting new User Lookup Table..")
    identify.lookup = getLookupTable()

  #lookup = getLookupTable()

  if(username in identify.lookup):
    return identify.lookup[username]
  else:
    return 'N/A'
identify.lookup = dict()
