import json, logging
from report_to_beam_proxy import reportToBeamProxy
from vars import SITE_NAME, ZABBIX_API_TOKEN
#from get_host_ID import getHostID
def createTrigger(triggers):
    
    # Define JSON payload with data to create the item
    data = json.dumps({
    "url" : "ZABBIX_API_URL",
    "payload" : {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": triggers,
            "auth": ZABBIX_API_TOKEN,
            "id": 2
        },
    })
    
    # Send the JSON payload to the Zabbix API using reportToBeamProxy
    response = reportToBeamProxy(data, metadata= "Create " + str(len(triggers)) +  " Trigger(s) for Host " + SITE_NAME)
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])
    
    # Check if the item was successfully created
    if "result" in json_body:
        #logging.info(service.displayName + " - Item erfolgreich erstellt")
        return
    else:
        logging.error(f"Fehler beim Erstellen der Trigger - {json_body['error']}")
