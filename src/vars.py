from os import environ

def prepare_vars(vars):
     missingvars = []
     for var in vars:
         env = environ.get(var)
         if env == None:
             missingvars.append(var)
         globals()[var] = environ.get(var)

     if(len(missingvars) > 0):
         raise Exception("Please define variables: %s" % (", ".join(missingvars)) )

prepare_vars(["PROJECT", "SITE_NAME", "HOST", "BEAM_URL", "PROXY_ID", "KEY", "MONITORING_TARGET"])

# system environment variables
SITE_NAME = environ.get("SITE_NAME")

PROJECT = environ.get("PROJECT")

HOST = environ.get("HOST")

BEAM_URL = environ.get("BEAM_URL")

PROXY_ID = environ.get("PROXY_ID")

KEY = environ.get("KEY")

MONITORING_TARGET = environ.get("MONITORING_TARGET")


HOST_CHECKINTERVAL = 540

# icinga settings

HOST_TEMPLATE = "bridgetest"

SERVICE_TEMPLATE = "bridgehead-service-daily"

