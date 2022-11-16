from wsgiref import headers
import requests, time
from vars import BEAM_URL, PROXY_ID, KEY, MONITORING_TARGET
import uuid
import json 
import base64

def reportToBeamProxy(payload):
    print("Sending Info")

    url = BEAM_URL + "/v1/tasks"
    auth = "ApiKey " + PROXY_ID + " " + KEY
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : auth
    }

    body = {
        "id": str(uuid.uuid4()),
        "from": PROXY_ID,
        "to": [
            MONITORING_TARGET
              ],
        "body": str(base64.b64encode(payload.encode('ascii'))),
        "failure_strategy": {
            "retry": {
                "backoff_millisecs": 1000,
                "max_tries": 5
            }
        },
        "ttl": 120,
        "metadata": ""
    }

    json_data=json.dumps(body)

    try:
        print("Start posting")
        response = requests.request("POST", url, headers=headers, data=json_data)
        
        # wenn status code != 200 dann Fehler
    except:
        raise SystemExit(time.ctime() + " error in reportToBeamProxy: not available")
    
    if response.status_code != 200:
        print(time.ctime() + " " + str(response.status_code))
