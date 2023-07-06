import json, logging, time, sys
from vars import SITE_NAME, ZABBIX_API_TOKEN
from report_to_beam_proxy import reportToBeamProxy
from create_host import createHost

global HOSTID

def getHostID():
    
    data = json.dumps({
        "url" : "ZABBIX_API_URL",

        "payload" : {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
            "hostid",
            "host"
            ]
        },
        "auth": ZABBIX_API_TOKEN,
        "id": 1
        }
    })

    #logging.info("Get HostID for " + SITE_NAME)
    
    response = reportToBeamProxy(data, metadata="Get HostID - " + SITE_NAME)
    
    if response == None:
        logging.error("Failed to establish a connection to Beam.")      
        sys.exit()
    
# Extract the JSON data from the response
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])
    
    hostID = [response["hostid"] for response in json_body["result"] if response["host"] == SITE_NAME]
    
    if not hostID:
        logging.warning("No host with Name " + SITE_NAME)
        createHost()
        return getHostID()  

    return hostID[0]

if not 'HOSTID' in globals():
    HOSTID = getHostID()
else:
    pass

