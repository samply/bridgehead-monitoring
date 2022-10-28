import requests
from vars import SITE_NAME, SERVER_URL
import time
from icingaAuth import headers

def compareServices(services):
    url = SERVER_URL + "v1/objects/services?filter=host.name==\"BK " + SITE_NAME + "\""

    payload = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except:
        raise SystemExit(time.ctime() + " error in compareServices: Icinga not available")


    icinga_services = [name['attrs']['name'] for name in response.json()['results']]

    project_services = [service.servicename for service in services.services]

    for icinga_service in icinga_services:
        if icinga_service not in project_services:
            url = SERVER_URL + "v1/objects/services/BK " + SITE_NAME + "!" + icinga_service + "?cascade=1"
            payload={}
            try:
                response = requests.request("DELETE", url, headers=headers, data=payload)
            except:
                raise SystemExit(time.ctime() + " Icinga not available")
            print(time.ctime() + " compare_checks:" + icinga_service + " status_code: %s" % response.json()['results'][0]['code'] + " " + response.json()['results'][0]['status'] )
            


        

