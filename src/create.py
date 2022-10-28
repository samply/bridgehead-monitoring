import json
import requests, time
from icingaAuth import headers
from common import Service
from vars import SERVER_URL, SITE_NAME, HOST_TEMPLATE, SERVICE_TEMPLATE

def createObj(obj=""):
    if isinstance(obj, Service):
        url = SERVER_URL + "v1/objects/services/BK " + SITE_NAME + "!" + obj.servicename
        payload = "{ \"templates\": [ \"" + SERVICE_TEMPLATE + "\" ], \"attrs\": { \"display_name\": \""+ obj.displayName + "\" } }"
    else:
        url = SERVER_URL + "v1/objects/hosts/BK " + SITE_NAME
        payload = "{ \"templates\" : [ \"" + HOST_TEMPLATE + "\"]}"

    try:
        response = requests.request("PUT", url, headers=headers, data=payload)
    except:
        print(time.ctime() + "error in createObj: not created, icinga not available")
        return
 
    try:
        print(time.ctime() + " createObj status_code: %s" % response.json()['results'][0]['code'] + " " + response.json()['results'][0]['status'] )
    except:
        print(str(response.json()['error']) + " " + response.json()['status'])
        return