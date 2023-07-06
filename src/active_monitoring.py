import time, requests, logging
from check_service import checkService
from active_send_back_to_beam import sendBackToBeam

from vars import BEAM_URL, beam_headers    

# Check for an active monitoring task in Beam
def checkForTask():
    wait_url = BEAM_URL + "v1/tasks?filter=todo&wait_count=1"
    payload = {}
    start = time.time()
    try:
        response = requests.request("GET", wait_url, headers=beam_headers, data=payload)
    except Exception as e:
        logging.error(str(e) + " Url used for GET request = " + wait_url)
        return None
    
    # If there is no response for more than 30 seconds, return None
    if response.status_code == 502:
        end = time.time() 
        logging.warning("GET timeout after " + str(end-start) + "s")
        return None
    
    # If the response is successful (status code 200), search for the active monitoring task
    if response.status_code == 200:
        for task in response.json():
            try:
                # Check if the task is for active monitoring
                if task["metadata"][0] == "active_monitoring":
                    return task
            except:
                continue
    return None

# Perform the active monitoring task for a specific service
def performTask(task, services):
        
    for service in services.services:
        if service.displayName == task["body"]:
            logging.info("Recieved active check for " + service.displayName )
            payload = checkService(service)
            sendBackToBeam(task["id"], task["from"], str(payload))
            return
        
    logging.warning("Recieved active check for " + task["body"] + " item does not exist")
    sendBackToBeam(task["id"], task["from"], task["body"] + " Item does not exist")
    return
    
    
    
    
# Continuously monitor for active monitoring tasks
def activeMonitoring(services):
    while True:
        task = None
        # Continuously check for new tasks until one is found
        while task is None:
            task = checkForTask()
            if task is None:
                # If no task is found, wait 1 second before checking again to conserve resources
                time.sleep(1)
        performTask(task, services)