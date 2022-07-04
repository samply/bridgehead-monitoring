class Service:
    def __init__(self, group, servicename, displayName, url, output, checkInterval):
        self.group = group
        self.servicename = servicename
        self.displayName = displayName
        self.url = url
        self.output = output
        self.checkInterval = checkInterval

class Host:
    def __init__(self, url, checkInterval):
        self.url = url 
        self.checkInterval = checkInterval