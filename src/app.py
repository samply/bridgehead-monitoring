import time
from importlib import import_module 
from myThread import MyThread
from vars import PROJECT
from report_to_beam_proxy import reportToBeamProxy
from check_service import checkService

services = import_module("projects.%s" % (PROJECT.lower()))

#wait for system to start up
time.sleep(2)

threads = []

#start host thread
h = MyThread()
h.name = "host-thread"
threads.append(h)
h.start()

time.sleep(5)

#check if services were deleted
#compareServices(services)

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
    
            
