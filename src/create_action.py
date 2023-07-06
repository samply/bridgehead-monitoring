import json, logging
from get_host_ID import HOSTID
from vars import ZABBIX_API_TOKEN, SITE_NAME
from report_to_beam_proxy import reportToBeamProxy


def create_action(userid):
    
    
# Create the JSON payload for the API request
    data = json.dumps({
        "url" : "ZABBIX_API_URL",
        "payload" : {
            'jsonrpc': '2.0',
            'method': 'action.create',
            'params': {
                'name': 'Alarm for item trigger - ' + SITE_NAME,
                'eventsource': 0,
                'status': 0,
                'esc_period': 120,
                'filter': {
                    'evaltype': 0,
                    'conditions': [
                        {
                            'conditiontype': 4,
                            'operator': 5,
                            'value': 2
                        },
                        {
                            "conditiontype": 1,
                            "operator": 0,
                            "value": HOSTID
                            }
                    ]
                },
                'operations': [
                *[
                    {'operationtype': 0, 'opmessage_usr': [{'userid': uid}], 'opmessage': {'default_msg': 1, 'mediatypeid': '1'}} 
                    for uid in userid
            ]]
            },
            'auth': ZABBIX_API_TOKEN,
            'id': 1
        }
    })

    response = reportToBeamProxy(data, metadata="Create action for " + SITE_NAME)
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])
    
    # Check if the item was successfully created
    if "result" in json_body:
        logging.info("Action created successfully")
        return
    else:
        logging.error(f"Error creating the action - {json_body}")
        
def check_existing_action(userids):
    data = json.dumps({
        'url' : 'ZABBIX_API_URL',
        'payload' : {
        'jsonrpc': '2.0',
        'method': 'action.get',
        'params': {
            'filter': {'name': 'Alarm for item trigger - ' + SITE_NAME},
            'output': ['name']
        },
        'auth': ZABBIX_API_TOKEN,
        'id': 1
    }})

    response = reportToBeamProxy(data, metadata="Get all actions for " + SITE_NAME)
    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])

    if 'result' in json_body and json_body['result']:
        logging.info("Action with name 'Alarm for item trigger - {}' already exists.".format(SITE_NAME))
    else:
        logging.info("Action with name 'Alarm for item trigger - {}' does not exist.".format(SITE_NAME))
        create_action(userids)
        