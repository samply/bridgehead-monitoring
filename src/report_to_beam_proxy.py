import requests, json, logging, time, sys
from uuid import uuid4
from vars import PROXY_ID, MONITORING_TARGET, BEAM_URL, SITE_NAME, beam_headers
from http.client import responses


def reportToBeamProxy(payload, metadata):
    # Generate a unique ID for the task
    taskID = str(uuid4())
    
    # Set the URLs for the POST and GET requests
    post_url = BEAM_URL + "v1/tasks"
    get_url =  BEAM_URL  + "v1/tasks/" + taskID + "/results?wait_count=1"
    
    # Create the body of the POST request in JSON format
    body = json.dumps({
        "id": taskID,
        "from": PROXY_ID,
        "to": [
            MONITORING_TARGET
              ],
        "body": payload,
        "failure_strategy": {
            "retry": {
                "backoff_millisecs": 1000,
                "max_tries": 5
            }
        },
        "ttl": "60s",
        "metadata": ["passive_monitoring", metadata, SITE_NAME]
    })
        
    MAX_CONNECTION_ATTEMPTS = 4

    for count in range(MAX_CONNECTION_ATTEMPTS, 0, -1):
        try:
            # Send a POST request to the monitoring system via the proxy
            post_response = requests.request("POST", url=post_url, headers=beam_headers, data=body)
            break  # Exit the loop if the request is successful
    
        except requests.exceptions.RequestException as e:
            if count == 1:
                logging.error(str(e))
                return None    
            logging.warning("Failed to connect to Beam - retry in 10s")
   
            time.sleep(10)
    
    if post_response.status_code == 201:
        # If the POST request is successful, send a GET request to get the task results
        #logging.info(metadata + " - task created successfully")
        try:
            get_response = requests.request("GET", get_url, headers=beam_headers)
        except Exception as e:
            logging.error(metadata + " " + str(e) + + " Url used for GET request = " + get_url)
            return None
        
    else:
        logging.error("Creating task failed - " + str(post_response.status_code) + " - " + responses[post_response.status_code])
        return None
            
    if get_response.status_code == 502:
            logging.error("Connection timed out - no response from report2Zabbix")
            return None
    # If the GET request is successful, check the task metadata and return the response
    elif get_response.status_code == 200:
        if get_response.json()[0]["metadata"] == "failed":
            logging.error(get_response.json()[0]["body"])
            return None
        elif get_response.json()[0]["metadata"] == "succeeded":
            return get_response
        elif get_response.json()[0]["metadata"] == "partially failed":
            logging.error(get_response.json()[0]["body"] + " - Check Item and Item-Key on Zabbix Website and try again.")
            return get_response
    else:
        logging.error("Receiving task failed: " + str(get_response.status_code) + " - " + responses[get_response.status_code])
        return None
        
        
        

