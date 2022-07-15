import requests, json
import time
from icingaAuth import headers
from ReportToMonitoring import reportToMonitoring
from vars import SITE_NAME, SERVER_URL, HOST_CHECKINTERVAL

def checkHost():
    while True:
        url = SERVER_URL + "v1/objects/hosts?host=BK " + SITE_NAME
        try:
            response = requests.request("GET", url, headers=headers)

        except:
            print(time.ctime() + " icinga not available")
            time.sleep(HOST_CHECKINTERVAL)
            continue
        break
    
    if response.status_code == 404:
        return response.status_code

    payload = { "type": "Host", 
                "filter": "host.name==\"BK " + SITE_NAME + "\"", 
                "exit_status": 0,
                "plugin_output": "ok"
                 }
    
    reportToMonitoring(json.dumps(payload))
    
