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

prepare_vars(["PROJECT", "SITE_NAME", "HOST", "SERVER_URL"])

SITE_NAME = environ.get("SITE_NAME")

PROJECT = environ.get("PROJECT")

HOST = environ.get("HOST")

SERVER_URL = environ.get("SERVER_URL")

HOST_CHECKINTERVAL = 540