import requests, json, sys, logging
from http.client import responses
from vars import SITE_NAME
from report_to_beam_proxy import reportToBeamProxy

def get_value_by_path(data, path):
    # If the path parameter is empty, return the text of the input data object
    if not path:
        return data.text
    # Try to parse the input data object as JSON
    try:
        data = data.json()
    except:
    # If an error occurs during parsing, log a warning message and return None
        logging.warning("No data because of wrong path " + str(path))
        return None
    # Iterate through each key in the path parameter
    for key in path:
    # If the key exists in the data object, update the data object to its value
        if key in data:
            data = data[key]
    # If the key does not exist in the data object, log a warning message and return None
        else:
            logging.warning("No data because of wrong path " + str(path))
            return None
    return str(data)

# A function that takes in a Service object
def checkService(service):
    
    logging.info("Checking Service " + service.url)
    payload = {
        "url" : "ZABBIX_SERVER_URL",
        "key" : service.key
        }
    # Attempting to send a GET request to the Service's URL with the Service's headers
    try:
        response = requests.request("GET", service.url, headers=service.headers)
    except Exception as e:
        logging.warning(service.displayName + " " + str(e))
        payload["status"] = "Error: connect ECONNREFUSED - " + service.url
    # If the caller of the function is `performTask`, return the updated payload dictionary
        if sys._getframe(1).f_code.co_name == "performTask":
            return payload
        return reportToBeamProxy(json.dumps(payload), metadata="Service - " + service.displayName + " - Error: connect ECONNREFUSED - " + service.url)
    
    # If the request was successful, update the payload dictionary to reflect the status of the Service 
    # by getting the value of the output key in the Service object using the `get_value_by_path` function
    
    try:
        if response.status_code >= 200 and response.status_code < 300: 
            payload["status"] = get_value_by_path(response, service.output)   
            logging.info(service.displayName + " - " + str(response.status_code) + " - " +  str(payload["status"]))
        else:
            payload["status"] = get_value_by_path(response, service.output) + " " + str(response.status_code)
            logging.info(service.displayName + " - " + str(response.status_code) + " - " +  str(payload["status"]))
            
    except:
        payload["status"] = get_value_by_path(response, service.output)   
        logging.warning(service.displayName + " - " + str(response.status_code) + " - " +  str(payload["status"]))
        
    # If the caller of the function is `performTask`, return the updated payload dictionary
    if sys._getframe(1).f_code.co_name == "performTask":
        return payload
    
    response = reportToBeamProxy(json.dumps(payload), metadata="check service - " + service.displayName + " - " + SITE_NAME)
    
    if response == None:
        logging.error("No response from beam - next attempt after the expiration of the update interval - " + service.displayName) 
    else:
        logging.info(service.displayName + " - " + str(response.json()[0]["body"]))
        