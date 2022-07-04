import requests, json, time
from ReportToMonitoring import reportToMonitoring

def checkBlaze(service, SITE_NAME):
    
    payload ={
            "type": "Service",
            "filter": "host.name==\"BK " + SITE_NAME + "\" && service.name==\"" + service.servicename + "\""
            #"exit_status": 2,
            #"plugin_output": "blaze nicht erreichbar"
        }
    headers = {}
    try:
        response = requests.request("GET", service.url, headers=headers, data=payload)

    except:
        payload["exit_status"] = 2
        payload["plugin_output"] = "blaze nicht erreichbar"
        print(time.ctime() + " " + service.servicename +  ": blaze nicht erreichbar")
        reportToMonitoring(json.dumps(payload), service, SITE_NAME)
        return

    print(time.ctime() + " " + service.servicename +  " status code: %s" % response.status_code)

    payload["exit_status"] = 0
    payload["plugin_output"] = eval("response." + service.output)

    reportToMonitoring(json.dumps(payload), service, SITE_NAME)
