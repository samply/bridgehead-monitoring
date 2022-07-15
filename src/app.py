import threading
import time
from importlib import import_module 
from create import createObj
from myThread import MyThread
from check_host import checkHost
from vars import PROJECT, SITE_NAME


services = import_module("projects.%s" % (PROJECT.lower()))

#wait for system to start up
time.sleep(20)

#check first if host exist
if checkHost() == 404:
    print(time.ctime() + " host not found, create new host: " + SITE_NAME)
    createObj()
    for service in services.services:
      createObj(service)

threads = []

#start host thread
h = MyThread()
h.name = "host-thread"
threads.append(h)
h.start()

#start service threads
for service in services.services:
    s = MyThread(service)
    s.name = service.servicename
    s.start()
    threads.append(s)
    time.sleep(25)

while True:
    for thread in threads:
        if not thread.is_alive():
            for t in threads: 
                t.stop()
            raise SystemExit(time.ctime() + " " + thread.name + " an error occured here.")        
        time.sleep(600)
    
            
