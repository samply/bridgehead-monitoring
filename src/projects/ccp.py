import requests, logging
from importlib import import_module
from vars import BLAZE_URL, BEAM_URL

blaze = import_module("projects.components.blaze")
blaze_url = BLAZE_URL #"http://localhost:8080"

beam_proxy = import_module("projects.components.beam-proxy")
beam_proxy_url = BEAM_URL #"http://localhost:8082"

components = [(blaze, blaze_url), (beam_proxy, beam_proxy_url)]

services = []

for comp, comp_url in components:
    try:
        requests.head(comp_url)
    except:
        logging.warning(comp_url + " is not reachable")
        continue
    logging.info(comp_url + " is reachable")
    services += comp.services
        
for service in services:
    if service.group == 'Blaze':
        service.url = blaze_url + service.url
    elif service.group == 'Beam-Proxy':
        service.url = beam_proxy_url + service.url
               
    logging.info("Monitoring: " + service.url)




