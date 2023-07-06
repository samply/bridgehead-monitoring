import logging
from cerate_item import createItem
from create_trigger import createTrigger
from get_zabbix_items import getZabbixItems
from vars import SITE_NAME
from get_host_ID import HOSTID

def compareItems(services):
    
    # Get existing Zabbix items and hostID
    zabbixItems, _ = getZabbixItems()
    
    items = []
    triggers = []
    item_created = 0
    # Compare each service's display name to existing Zabbix items
    for service in services.services:
        if service.displayName not in zabbixItems:
            # Create item if it doesn't exist in Zabbix
            item = {
                "name": service.displayName,
                "key_": service.key,
                "hostid": HOSTID,
                "interfaceid": "0",
                "type": 2,
                "value_type": 4,
                "delay": 0         
            }
            items.append(item)
            item_created += 1
            
            if service.trigger:
                service.trigger["expression"] = service.trigger["expression"].replace('SITE_NAME/itemkey', SITE_NAME + "/" + service.key)      
                triggers.append(service.trigger)
    
    # Log the number of items created, if any
    if item_created > 0:
        createItem(items)
        logging.info(str(item_created) + " items added for " + SITE_NAME)
        if len(triggers) > 0:
            createTrigger(triggers)
    else:
        logging.info("No new Items added for " + SITE_NAME)
        

