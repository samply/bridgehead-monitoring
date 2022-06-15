import imp
import requests
import time
from icingaAuth import headers

def createHost(SITE_NAME):
    url = "http://e260-serv-07/v1/objects/hosts/BK " + SITE_NAME

    adress = SITE_NAME.split()[0].lower() + ".bk.a.ccp-it.dktk.dkfz.de"
    payload = "{ \"templates\" : [\"bridgetest\"], \"attrs\": { \"address\": \"" + adress + "\",\"check_command\": \"dummy\"\r\n}}"   
    try:
        response = requests.request("PUT", url, headers=headers, data=payload)
    except:
        print(time.ctime() + " createHost: " + SITE_NAME + " not created, icinga not available")
        return
    
    print(time.ctime() + " createHost status_code: %s" % response.json()['results'][0]['code'] + " " + response.json()['results'][0]['status'] )
    
        
def createService(SITE_NAME, service):

    url = "http://e260-serv-07/v1/objects/services/BK " + SITE_NAME + "!" + service.servicename
    payload = "{ \"templates\": [ \"bridgehead-service-daily\" ], \"attrs\": { \"display_name\": \""+ service.displayName + "\" } }"
    try:
        response = requests.request("PUT", url, headers=headers, data=payload)
    except:
        print(time.ctime() + "error createService: " + service.serviname + " not created, icinga not available")
        return

    print(time.ctime() + " createService status_code: %s" % response.json()['results'][0]['code'] + " " + response.json()['results'][0]['status'] )
    