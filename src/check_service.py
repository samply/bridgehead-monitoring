import requests, json, time
from vars import SITE_NAME
from report_to_beam_proxy import reportToBeamProxy

def checkService(service):
    
    print(time.ctime() + ": Checking Service " + service.url)

    payload ={
            "type": "Service",
            "hostname": SITE_NAME,
            "servicename": service.servicename,
        }
    headers = {
        "Content-Type": "application/json"
            }
    try:
        response = requests.request("GET", service.url, headers=headers)

    except:
        payload["output_code"] = 503
        payload["output_text"] = "Service Unavailable"
        print(time.ctime() + " " + service.servicename + "(400): Could not send request / Error: connect ECONNREFUSED")
        reportToBeamProxy(json.dumps(payload))
        return

    print(time.ctime() + " " + service.servicename +  ": " + str(response.status_code))

    payload["output_code"] = response.status_code
    payload["output_text"] = response.text

    reportToBeamProxy(json.dumps(payload))