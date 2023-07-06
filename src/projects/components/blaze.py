from common import Service

headers = {
        "Content-Type": "application/json"
            }

# more trigger information: https://www.zabbix.com/documentation/current/en/manual/api/reference/trigger/object#trigger

blaze_health_trigger = {
            "description": "Blaze: Health Check",
            "event_name" : "Balze not running",
            "expression": "last(/SITE_NAME/itemkey)<>\"OK\"",
            "priority" : 4
        }

services = [
    Service("Blaze", "blaze-health", "blazehealth.item", "Blaze: Health", "/health", [], 360, headers, blaze_health_trigger),
    Service("Blaze", "blaze-version", "blazeversion.item", "Blaze: Version", "/fhir/metadata", ['software','version'], 360, headers, None),
    Service("Blaze", "blaze-resources", "blazeresouces.item", "Blaze: Ressourcen", "/fhir", ['total'], 360, headers, None)
]