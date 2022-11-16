import time
from importlib import import_module 
from myThread import MyThread
from vars import PROJECT
from report_to_beam_proxy import reportToBeamProxy
from check_service import checkService

services = import_module("projects.%s" % (PROJECT.lower()))
print(time.ctime() + " Loaded Project " + PROJECT)

time.sleep(25)

print(time.ctime() + " Starting Monitoring")

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

while True:
    for thread in threads:
        if not thread.is_alive():
            for t in threads: 
                t.stop()
            raise SystemExit(time.ctime() + " " + thread.name + " an error occured here.")
    time.sleep(600)
    
            
