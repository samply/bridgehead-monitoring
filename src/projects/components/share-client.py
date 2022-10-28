from common import Service


services = [
    #Service("Teiler", "share-client", "Teiler", "/rest/monitoring/check", "json()", 7200),
    #Service("Teiler", "bridgehead-teiler-version", "Teiler: Version", "/rest/monitoring/version", "json()", 7200),
    Service("Teiler", "bridgehead-patients-total", "Anzahl Patienten mit Standort-ID", "/rest/monitoring/patients-total", "json()['status_text']", 60),
    Service("Teiler", "bridgehead-patients-dktkflagged", "Anzahl Patienten DKTK", "/rest/monitoring/patientsdktkflagged", "json()['status_text']", 72),
    #Service("Teiler", "bridgehead-referencequery-resultcount", "Referenzquery: Ergebniszahl", "/rest/monitoring/referencequery-resultcount", "json()", 7200),
    #Service("Teiler", "bridgehead-referencequery-duration", "Referenzquery: Ausfuehrzeit", "/rest/monitoring/referencequery-duration", "json()", 7200),
    Service("Teiler", "bridgehead-job-config", "Job Konfigurationen", "/rest/monitoring/job-config", "json()['status_text']", 72),
    #Service("Teiler", "bridgehead-ldm", "ldm", "/rest/monitoring/bridgehead-ldm", "json()", 7200)


]