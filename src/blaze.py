from common import Service
from os import environ

SITE_NAME = "Bielefeld (A)"

# def prepare_vars(vars):
#     missingvars = []
#     for var in vars:
#         env = environ.get(var)
#         if env == None:
#             missingvars.append(var)
#         globals()[var] = environ.get(var)

#     if(len(missingvars) > 0):
#         raise Exception("Please define variables: %s" % (", ".join(missingvars)) )

#prepare_vars(["PROJECT", "SITE_NAME", "HOST"])

services = [
    Service("Blaze", "blaze-health", "Blaze: Health", SITE_NAME, "http://localhost:8080/health", "text"),
    Service("Blaze", "blaze-version", "Blaze: Version", SITE_NAME, "http://localhost:8080/fhir/metadata", "json()['software']['version']"),
    Service("Blaze", "blaze-resources", "Blaze: Verbrauchte Ressourcen", SITE_NAME, "http://localhost:8080/fhir", "json()['total']"),
    Service("Blaze", "blaze-date", "Blaze: Datum", SITE_NAME, "http://localhost:8080/fhir/metadata", "json()['date']")
]
