import requests, json
import time
from icingaAuth import headers
from report_to_monitoring import reportToMonitoring
from vars import SITE_NAME, SERVER_URL
from create import createObj
from status_code import statusCode

def checkHost():
    url = SERVER_URL + "v1/objects/hosts?host=BK " + SITE_NAME
    try:
        response = requests.request("GET", url, headers=headers)

    except:
        raise SystemExit(time.ctime() + " error in checkHost: Icinga not available")
    
    if response.status_code == 404:
        print(time.ctime() + " " + statusCode(response.status_code) +", create new host: " + SITE_NAME)
        createObj()
    elif response.status_code != 200:
        print(time.ctime() + " " + statusCode(response.status_code))
        return


    payload = { "type": "Host", 
                "filter": "host.name==\"BK " + SITE_NAME + "\"", 
                "exit_status": 0,
                "plugin_output": "ok"
                 }
    
    reportToMonitoring(json.dumps(payload))
    
