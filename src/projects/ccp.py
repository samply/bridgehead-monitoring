import time
from importlib import import_module

blaze = import_module("projects.components.blaze")

services = []

services += blaze.services

for service in services:
    if service.group == 'Blaze':
        adress = "http://bridgehead-ccp-blaze:8080"

    service.url = adress + service.url
    print(time.ctime() + " Monitoring: " + service.url )




