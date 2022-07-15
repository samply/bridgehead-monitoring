from common import Service


services = [
    Service("Blaze", "blaze-health", "Blaze: Health", "http://localhost:8080/health", "text", 7200),
    Service("Blaze", "blaze-version", "Blaze: Version", "http://localhost:8080/fhir/metadata", "json()['software']['version']", 7200),
    Service("Blaze", "blaze-resources", "Blaze: Verbrauchte Ressourcen", "http://localhost:8080/fhir", "json()['total']", 7200),
]