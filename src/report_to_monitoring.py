import requests, sys, time, json
from create import createObj
from icingaAuth import headers
from vars import SERVER_URL
from status_code import statusCode

def reportToMonitoring(payload, service=""):
    url = SERVER_URL + "v1/actions/process-check-result"
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        raise SystemExit(time.ctime() + " error in reportToMonitoring: Icinga not available")
    
    if response.status_code == 500 and service != "": 
        print(time.ctime() + " " + service.servicename + " does not exist: create service " + service.displayName)
        createObj(service)
        return reportToMonitoring(payload, service)

    elif  response.status_code != 200:
        print(time.ctime() + " reportToMonitoring: " + statusCode(response.status_code))
        return
    print(time.ctime() + " reportToMonitoring: StatusCode %d" % response.status_code + " " + response.json()['results'][0]['status'])


    