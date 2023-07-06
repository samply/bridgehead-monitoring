from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, start_http_server, generate_latest, CONTENT_TYPE_LATEST, Gauge
from item_handler import itemHandler
from get_zabbix_items import getZabbixItems
from vars import SITE_NAME
import json
import logging

app = Flask(__name__)

# Define a counter for the number of POST requests received
POST_COUNTER = Counter('myapp_post_requests_total', 'Number of POST requests received')

# Define a counter for the number of successful POST requests
SUCCESSFUL_POST_COUNTER = Counter('myapp_successful_requests_total', 'Number of successful POST requests received')

# Define a gauge for the number of current requests
CURRENT_REQUESTS_GAUGE = Gauge('myapp_current_requests', 'Number of current requests being processed')


@app.route('/monitoring', methods=['POST'])
def post_data():
    # Increment the counter for the number of POST requests received
    POST_COUNTER.inc() 
    # Increment the gauge for the number of current requests
    CURRENT_REQUESTS_GAUGE.inc()
    data = request.get_json()
    
    # Validate the required fields in the received data
    required_fields = ["item", "key", "status"]
    for field in required_fields:
        if field not in data:
            return "Value " + field + " is missing in  " + json.dumps(data), 422
    
    # Überprüfen, ob das Feld 'priority' den erwarteten Wert hat
    priority = data.get("priority", "low")
    if priority not in ["low", "medium", "high"]:
        return "Invalid priority value: " + json.dumps(data), 422
    
    logging.info("Received new data to report from " + data["item"] + " - priority " + data["priority"])
    
    # Define the expected Zabbix items
    zabbixItems, zabbixItemKeys = getZabbixItems()
    
    zabbixDict = dict(zip(zabbixItems, zabbixItemKeys))
    
    # Validate if the received item is in the expected Zabbix items
    if data["item"] in zabbixDict:
        if zabbixDict[data["item"]] != data["key"]:
            return "Item Key for '"+ data["item"] + "' does not match the item key", 404
    else:
        return "Item '"+ data["item"] + "' was not found, create a Trapper Item on www.zabbix.com for Host '" + SITE_NAME + "', with Item key \'" + data["key"] + "\'. Make sure to check if the key is already being used by another item.", 404
    # Handle the received data
    itemHandler(data)
    
    SUCCESSFUL_POST_COUNTER.inc()
    
    # Decrement the gauge for the number of current requests
    CURRENT_REQUESTS_GAUGE.dec()
    
    return jsonify({
        "message": "Data has been processed successfully.",
        "data": data
    })

@app.route('/metrics', methods=['GET'] )
def metrics():
    return Response(
        generate_latest(POST_COUNTER, SUCCESSFUL_POST_COUNTER, CURRENT_REQUESTS_GAUGE), 
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == '__main__':
    app.run(debug=False)
