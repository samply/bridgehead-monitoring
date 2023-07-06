import logging, json, sys
from vars import SITE_NAME, ZABBIX_API_TOKEN, HOST_GROUP
from report_to_beam_proxy import reportToBeamProxy

# Define JSON payload with data to create the host
def createHost():
    
    get_host_group = json.dumps({
        'url': "ZABBIX_API_URL",
        'payload': {
        'jsonrpc': '2.0',
        'method': 'hostgroup.get',
        'params': {
        "output": ["name", "groupid" ],
    },
    'auth': ZABBIX_API_TOKEN,
    'id': 2,
    }})
    
    # Send the JSON payload to the Zabbix API using reportToBeamProxy
    response = reportToBeamProxy(get_host_group, metadata="Get ID for Hostgroup " + HOST_GROUP)
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])
    
    hostids = {group["name"]: group["groupid"] for group in json_body["result"]}
    
    if HOST_GROUP in hostids:
        GROUPID = hostids[HOST_GROUP]
    else: 
        logging.error(f"Hostgroup '{HOST_GROUP}' not found, create Hostgroup on Zabbix and try again.")
        raise SystemExit()
    
    host_data = json.dumps({
        'url': "ZABBIX_API_URL",
        'payload': {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": SITE_NAME,
                "groups": [
                    {
                        "groupid": GROUPID
                    }
                ]
            },
            "auth": ZABBIX_API_TOKEN,
            "id": 2
        },
        })

    # Send the JSON payload to the Zabbix API using reportToBeamProxy
    response = reportToBeamProxy(host_data, metadata="Create Host " + SITE_NAME)
    
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])

    # Check if the host was successfully created
    if "result" in json_body:
        logging.info("Host created successfully")
    else:
        logging.error("Host could not be created - " + json_body)
