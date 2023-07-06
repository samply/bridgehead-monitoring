import time, sched, threading, logging, subprocess
from importlib import import_module 
from myThread import MyThread
from vars import PROJECT
from compare_items import compareItems
from active_monitoring import activeMonitoring
from notifications import check_user

#wait for other components
time.sleep(20)
# Load the current project
services = import_module("projects.%s" % (PROJECT.lower()))
logging.info("Loaded Project: " + PROJECT)

# Start the Flask API server on /monitoring
#api_process = subprocess.Popen(["python", "src\\flask_api.py", "--debug"])

time.sleep(2)

logging.info("Starting Monitoring")

time.sleep(2)

# Compare items in the services with Zabbix items
logging.info("Compare Items")
compareItems(services)

time.sleep(2)
logging.info("Check Notification Setting")
check_user()

time.sleep(5)
threads = []

# Start active monitoring thread
t = threading.Thread(target=activeMonitoring, args=(services,))
t.name = "active-check"
t.start()
threads.append(t)
time.sleep(2)
# Create processes for each service
for service in services.services:
    s = MyThread(service)
    s.name = service.servicename
    s.start()
    time.sleep(3)
    threads.append(s)

# Check if threads are still running
def check_threads():
    for thread in threads:
        for t in threads:
            try:
                t.stop()
            except:
                t.join()
            logging.error(f"{thread.name} an error occurred here.")
            exit()
    scheduler.enter(60, 1, check_threads)

# Create the scheduler to run the check threads function
scheduler = sched.scheduler(time.time, time.sleep)       
scheduler.enter(0, 1, check_threads)
scheduler.run()
