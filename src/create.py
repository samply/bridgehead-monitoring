import requests, time
from icingaAuth import headers
from common import Service
from vars import SERVER_URL, SITE_NAME

def createObj(obj=""):

    if isinstance(obj, Service):
        url = SERVER_URL + "v1/objects/services/BK " + SITE_NAME + "!" + obj.servicename
        payload = "{ \"templates\": [ \"bridgehead-service-daily\" ], \"attrs\": { \"display_name\": \""+ obj.displayName + "\" } }"
        print(time.ctime() + " create new service: " + obj.displayName)

    else:
        url = SERVER_URL + "v1/objects/hosts/BK " + SITE_NAME
        payload = "{ \"templates\" : [\"bridgetest\"]}"

    try:
        response = requests.request("PUT", url, headers=headers, data=payload)
    except:
        print(time.ctime() + "error createObj: " + obj.servicename + " not created, icinga not available")
        return

    print(time.ctime() + " createObj status_code: %s" % response.json()['results'][0]['code'] + " " + response.json()['results'][0]['status'] )