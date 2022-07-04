from threading import Thread, Event
from check_blaze import checkBlaze
from check_host import checkHost
from common import Service

class MyThread(Thread):
    def __init__(self, comp, SITE_NAME):
        Thread.__init__(self)
        self.stopped = Event()
        self.comp = comp
        self.SITE_NAME = SITE_NAME

    def run(self):
        while not self.stopped.wait(self.comp.checkInterval):
            if isinstance(self.comp, Service):
                checkBlaze(self.comp, self.SITE_NAME)
            else:
                checkHost(self.comp, self.SITE_NAME)