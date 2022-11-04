from wsgiref import headers
import requests, time
from vars import BEAM_URL, PROXY_ID, KEY
from status_code import statusCode
import uuid

def reportToBeamProxy(payload):
    url = BEAM_URL + "/v1/tasks"
    auth = "ApiKey " + PROXY_ID + " " + KEY
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : auth
    }

    body = {
        "id": uuid.uuid4(),
        "from": PROXY_ID,
        "to": [
            PROXY_ID
              ],
        "body": payload,
        "failure_strategy": {
            "retry": {
                "backoff_millisecs": 1000,
            "max_tries": 5
            }
        },
        "ttl": 3600,
        "metadata": "The broker can read and use this field e.g., to apply filters on behalf of an app"
    }


    try:
        response = requests.request("POST", url, headers=headers, data=payload, body=body)
        # wenn status code != 200 dann Fehler
    except:
        raise SystemExit(time.ctime() + " error in reportToBeamProxy: not available")
    
    if response.status_code != 200:
        print(time.ctime() + " " + statusCode(response.status_code))
