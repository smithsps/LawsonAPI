import subprocess
import User

def who(host):
  ssh = subprocess.Popen(['ssh', '%s' % host, 'who'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return ssh
	
