from os import environ
import os
import logging, colorlog

'''def prepare_vars(vars):
     missingvars = []
     for var in vars:
         env = environ.get(var)
         if env == None:
             missingvars.append(var)
         globals()[var] = environ.get(var)

     if(len(missingvars) > 0):
         raise Exception("Please define variables: %s" % (", ".join(missingvars)) )

prepare_vars(["PROJECT", "SITE_NAME", "ZABBIX_URL", "ZABBIX_API_URL", "ZABBIX_API_TOKEN", "BEAM_URL", "PROXY_ID", "KEY", "MONITORING_TARGET"])

# system environment variables
PROJECT = "CCP" #environ.get("PROJECT") 

SITE_NAME = "Test Host" #"Test Host" #environ.get("SITE_NAME") 
#HOST = environ.get("HOST")

ZABBIX_API_TOKEN = "16000caad2bd0a528573a7d22a154a327eae04708ccf3e35854a3c97ff09d751"
#"74c5f3b8f3416b28c6d07e31c42db9a93c4b8b66a8d8371377ba17a2d3d96192""6c87e2319e1d527daa89601deb2448f03d40b10e750438964071dd6ed748811d"# produktiv #environ.get("ZABBIX_API_TOKEN")

BEAM_URL = "http://localhost:8082" #environ.get("BEAM_URL")

PROXY_ID = "zabbix.niclas-dev.broker.dev.ccp-it.dktk.dkfz.de" #environ.get("PROXY_ID")  

KEY = "1234" #environ.get("KEY")

MONITORING_TARGET = "zabbix.monitoring-central.broker.dev.ccp-it.dktk.dkfz.de" #"zabbix.niclas-dev.broker.dev.ccp-it.dktk.dkfz.de"  #environ.get("MONITORING_TARGET") 

HOST_GROUP = "Test Group"
#Components

BLAZE_URL = "http://localhost:8080"

BEAM_PROXY_URL = "http://localhost:8082"

BRIDGEHEAD_ADMIN = "niclas.krembsler@dkfz-heidelberg.de"
'''
PROJECT = os.environ['PROJECT']

SITE_NAME = os.environ['SITE_NAME']

#HOST = environ.get("HOST")

ZABBIX_API_TOKEN = os.environ['ZABBIX_API_TOKEN']

BEAM_URL = os.environ['BEAM_URL']

PROXY_ID = os.environ['PROXY_ID']

KEY = os.environ['KEY']

MONITORING_TARGET = os.environ['MONITORING_TARGET']

HOST_GROUP = os.environ['HOST_GROUP']

BRIDGEHEAD_ADMIN = os.environ['BRIDGEHEAD_ADMIN']

#Components

BLAZE_URL = os.environ['BLAZE_URL']

beam_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'ApiKey ' + PROXY_ID + " " + KEY
    }  

#set up logger

log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}
# Konfiguration des Logging-Handlers
handler = colorlog.StreamHandler()
formatter_str = '%(asctime)s | %(log_color)s%(levelname)s%(reset)s::%(funcName)s | %(message)s'
handler.setFormatter(colorlog.ColoredFormatter(formatter_str, log_colors=log_colors, reset=True, datefmt='%Y-%m-%d %H:%M:%S'))
logging.basicConfig(level=logging.INFO, handlers=[handler]) # Log-Level auf INFO setzen

logging.root.addHandler(handler)