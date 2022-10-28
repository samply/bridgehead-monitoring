from wsgiref import headers
import requests, time
from vars import BEAM_URL
from status_code import statusCode

def reportToBeamProxy(payload):
    url = BEAM_URL + "/v1/tasks"
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : "ApiKey test.niclas.broker.dev.ccp-it.dktk.dkfz.de 3128937asd7823hZ."
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        # wenn status code != 200 dann Fehler
    except:
        raise SystemExit(time.ctime() + " error in reportToBeamProxy: not available")
    
    if response.status_code != 200:
        print(time.ctime() + " " + statusCode(response.status_code))
