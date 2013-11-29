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
names.extend(lab_list('moore', 24))
names.extend(lab_list('sac', 12))
names.extend(lab_list('sslab', 24))

names.append('pod4-4')






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
