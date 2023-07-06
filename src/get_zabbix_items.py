import json, logging
#from get_host_ID import getHostID
from report_to_beam_proxy import reportToBeamProxy
from vars import ZABBIX_API_TOKEN, SITE_NAME
from get_host_ID import HOSTID


def getZabbixItems():
    
    #HOSTID = getHostID()
    data = json.dumps({
        'url': "ZABBIX_API_URL",
        'payload': {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": [
                    "itemid",
                    "name",
                    "key_"
                ],
                "hostids": HOSTID
            },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
        },
    })

    #print(time.ctime() + " | get all listet Items for " + SITE_NAME)
    #logging.info("Get all Items for " + SITE_NAME)
    
    response = reportToBeamProxy(data, metadata="Compare items - " + SITE_NAME)
    
    if response is None:
        logging.critical("Exit")
        exit()
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])

    zabbixItems = [response["name"] for response in json_body["result"]]
    zabbixItemKeys = [response["key_"] for response in json_body["result"]]
    
    return zabbixItems, zabbixItemKeys #HOSTID