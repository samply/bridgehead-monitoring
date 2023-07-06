class Service:
    def __init__(self, group, servicename, key, displayName, url, output, checkInterval, headers, trigger):
        self.group = group
        self.servicename = servicename
        self.key = key
        self.displayName = displayName
        self.url = url
        self.output = output
        self.checkInterval = checkInterval
        self.headers = headers
        self.trigger = trigger
        
