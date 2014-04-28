import discover
import User
import time
import sys

def lab_list(name, max):
  names = list()
  for i in range(max):
    names.append(name + '%02d' % i)

  return names

#Generate computer names to visit
names = list()
c = []
#Lawson
c.extend(("SAC%02d" % i, "LWSN B131")   for i in range(1,14)) #SAC LAB
c.extend(("MOORE%02d" % i, "LWSN B146") for i in range(0,25)) #MOORE LAB
c.extend(("SSLAB%02d" % i, "LWSN B158") for i in range(0,25)) #SSLAB LAB

#POD Lab
c.append(("POD0-0", "LWSN B148"))
#c.extend(("POD1-%d" % i, "LWSN B148") for i in range(1,6))
#c.extend(("POD2-%d" % i, "LWSN B148") for i in range(1,6))
#c.extend(("POD3-%d" % i, "LWSN B148") for i in range(1,6))
#c.extend(("POD4-%d" % i, "LWSN B148") for i in range(1,6))
#c.extend(("POD5-%d" % i, "LWSN B148") for i in range(1,6))

#HAAS
c.extend(("BORG%02d" % i, "HAAS G40") for i in range(0,25)) #BORG LAB
c.extend(("XINU%02d" % i, "HAAS 257") for i in range(0,22)) #Xinu Lab


names = [str(i[0]) for i in c]






#who_list returns list of [ name, process]
processes = discover.who_list(names)
completed = list()

#Lets time it
start_time = time.time()


# Wait for processes to finish, add them to completed when they're done
while processes:
  for p in processes:
    if(p[1].poll() is not None):
      completed.append(p)
      processes.remove(p)
    sys.stdout.write("Completed: {0}/{1}.  Time: {2:.5g} \r".format(len(completed), len(names),  time.time()- start_time))
    sys.stdout.flush()
  time.sleep(0.05)

sys.stdout.write("\n")
#print("Completed in %g secs" % (time.time() - start_time))

users = list()
for p in completed:
  who = p[1].stdout.readlines()
  for line in who:
    split = line.split()
    users.append(User.User(split[0], discover.identify(split[0]), ' '.join(split[2:5]), p[0] + '-' +  split[1]))

users.sort(key = lambda x:  x.locations)

for u in users:
  print(u)
