import logging, json
from report_to_beam_proxy import reportToBeamProxy
from vars import SITE_NAME

# Initialize an empty list to hold the items
zabbix_items = []

def itemHandler(data):
    zabbix_items.append(data)
    
    # Check the priority of the item
    if data["priority"] == "high" or len(zabbix_items) > 4:
        zabbix_data = {
            "url": "ZABBIX_SERVER_URL",
            "list": zabbix_items
        }
        response = reportToBeamProxy(json.dumps(zabbix_data), metadata="New data (" + str(len(zabbix_items)) + " item(s) ) from " + SITE_NAME)
        if response == None:
            logging.error("Data will be attempted to be resent when the next item is received.")
            return
        zabbix_items.clear()



