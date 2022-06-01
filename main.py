import requests
import time
from os import environ
import sched
from check_blaze import checkBlaze
from blaze import services, SITE_NAME
from create import createHost
from icingaAuth import headers

def checkHost(SITE_NAME):
    
    url = "http://e260-serv-07/v1/objects/hosts?host=BK " + SITE_NAME
    while True:
        try:
            response = requests.request("GET", url, headers=headers)

        except:
            print(time.ctime() + " icinga not available")
            time.sleep(7000)
            continue
        break 
    return response.status_code


#check icinga and create host if not exist
if checkHost(SITE_NAME) == 200:
  print(time.ctime() + " icinga available") 

elif checkHost(SITE_NAME)  == 404:
  print(time.ctime() + " host not found, create new host: " + SITE_NAME)
  createHost(SITE_NAME)

s = sched.scheduler(time.time, time.sleep)

while True:
  checkHost(SITE_NAME)
  for service in services:
    s.enter(10, 1, checkBlaze, (service, ))
  s.run()
