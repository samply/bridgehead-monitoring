import sys, pathlib
from importlib import import_module

blaze = import_module("projects.components.blaze")

share = import_module("projects.components.share-client")

services = []

adress = "http://bridgehead-ccp-blaze:8080"
#adress = "http://localhost:8080"

services += blaze.services
services += share.services


for service in services:
    if service.group == 'Blaze':
        adress = "http://localhost:8092"
    elif service.group == 'Teiler':
        adress = "http://localhost:8095"

    service.url = adress + service.url



