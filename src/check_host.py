import requests, json
import time
from icingaAuth import headers
from ReportToMonitoring import reportToMonitoring

def checkHost(host, SITE_NAME):
    while True:
        url = host.url + SITE_NAME
        try:
            response = requests.request("GET", url, headers=headers)

        except:
            print(time.ctime() + " icinga not available")
            time.sleep(host.checkInterval)
            continue
        break
    
    if response.status_code == 404:
        return response.status_code

    payload = { "type": "Host", 
                "filter": "host.name==\"BK " + SITE_NAME + "\"", 
                "exit_status": 0,
                "plugin_output": "OK"
                 }
    
    reportToMonitoring(json.dumps(payload), host)
    
