from common import Service


services = [
    Service("Blaze", "blaze-health", "Blaze: Health", "/health", "text", 7200),
    Service("Blaze", "blaze-version", "Blaze: Version", "/fhir/metadata", "json()['software']['version']", 7200),
    ##Service("Blaze", "blaze-resources", "Blaze: Verbrauchte Ressourcen", "/fhir", "json()['total']", 7200)
]