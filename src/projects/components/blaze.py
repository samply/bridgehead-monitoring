from common import Service


services = [
    Service("Blaze", "blaze-health", "Blaze: Health", "/health", "text", 480),
    Service("Blaze", "blaze-version", "Blaze: Version", "/fhir/metadata", "json()['software']['version']", 480)
    ##Service("Blaze", "blaze-resources", "Blaze: Ressourcen", "/fhir", "json()['total']", 7200)
]