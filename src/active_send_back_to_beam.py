import requests, json, logging
from vars import beam_headers, BEAM_URL, PROXY_ID
from http.client import responses

def sendBackToBeam(id, to, result):
    url = BEAM_URL + "v1/tasks/" + id + "/results/" + PROXY_ID
    
    payload = json.dumps({
      "from": PROXY_ID,
      "metadata": "The broker can read and use this field e.g., to apply filters on behalf of an app",
      "status": "succeeded",
      "body": result,
      "task": str(id),
      "to": [
        str(to)
      ]
    })

    try:
      response = requests.request("PUT", url, headers=beam_headers, data=payload)
    except Exception as e:
      logging.error(f"{e} Url used for PUT request = {url}")
    
    if response.status_code == 201:
      logging.info("Data for active check send to Beam successfully") 
      
    else:
      logging.error("Task could not be created " + str(response.status_code) + " " + str(responses[response.status_code]))