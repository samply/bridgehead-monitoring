import sys, pathlib
from importlib import import_module

blaze = import_module("projects.components.blaze")

services = []

adress = "http://bridgehead-ccp-blaze:8080"

services += blaze.services

for service in services:
    if service.group == 'Blaze':
        adress = "http://bridgehead-ccp-blaze:8080"

    service.url = adress + service.url



