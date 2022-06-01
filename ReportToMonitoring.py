import requests
import json
import time
from create import createService
from blaze import SITE_NAME
from icingaAuth import headers

def reportToMonitoring(payload, service):
    url = "http://e260-serv-07/v1/actions/process-check-result"

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        print(time.ctime() + " reportToMonitoring: icinga not available\n")
        return
    
    if response.status_code == 500: 
        print(time.ctime() + " " + service.servicename + " does not exist: create service...")
        createService(SITE_NAME, service)
        return reportToMonitoring(payload, service)
        
    print(time.ctime() + " reportToMonitoring: StatusCode %d" % response.status_code + " " + response.json()['results'][0]['status']+"\n")