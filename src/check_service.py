import requests, json, time
from vars import SITE_NAME
from status_code import statusCode
from report_to_beam_proxy import reportToBeamProxy

def checkService(service):
    
    payload ={
            "type": "Service",
            "filter": "host.name==\"BK " + SITE_NAME + "\" && service.name==\"" + service.servicename + "\""
        }
    headers = {}
    try:
        response = requests.request("GET", service.url, headers=headers, data=payload)

    except:
        payload["exit_status"] = 2
        payload["plugin_output"] = "Could not send request / Error: connect ECONNREFUSED"
        print(time.ctime() + " " + service.servicename + ": Could not send request / Error: connect ECONNREFUSED")
        reportToBeamProxy(json.dumps(payload))
        return

    print(time.ctime() + " " + service.servicename +  ": " + statusCode(response.status_code))

    if response.status_code == 200:
        payload["exit_status"] = 0
        payload["plugin_output"] = eval("response." + service.output)

    elif response.status_code != 200:
        payload["exit_status"] = 2
        payload["plugin_output"] = statusCode(response.status_code)

    reportToBeamProxy(json.dumps(payload))