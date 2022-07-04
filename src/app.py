import time
from ccp import services, host
from create import createObj
from myThread import MyThread
from check_host import checkHost
from check_blaze import checkBlaze
from os import environ

def prepare_vars(vars):
     missingvars = []
     for var in vars:
         env = environ.get(var)
         if env == None:
             missingvars.append(var)
         globals()[var] = environ.get(var)

     if(len(missingvars) > 0):
         raise Exception("Please define variables: %s" % (", ".join(missingvars)) )

prepare_vars(["PROJECT", "SITE_NAME", "HOST"])

SITE_NAME = environ.get("SITE_NAME")

#wait for system to start up
time.sleep(15)

#check first if host exist
if checkHost(host, SITE_NAME) == 404:
    print(time.ctime() + " host not found, create new host: " + SITE_NAME)
    createObj(host, SITE_NAME)
    for service in services:
      createObj(service, SITE_NAME)

for service in services:
  checkBlaze(service, SITE_NAME)

#start host thread
h = MyThread(host, SITE_NAME)
h.start()

#start service threads
for service in services:
  s = MyThread(service, SITE_NAME)
  s.start()
  time.sleep(25)

