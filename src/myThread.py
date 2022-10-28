from concurrent.futures import thread
import time
from threading import Thread, Event
from check_service import checkService
from check_host import checkHost
from common import Service
from vars import HOST_CHECKINTERVAL

class MyThread(Thread):
    def __init__(self, comp=""):
        Thread.__init__(self)
        self.stopped = Event()
        self.comp = comp

    def run(self):
        while not self.stopped.isSet():
            if isinstance(self.comp, Service):
                checkService(self.comp)
                self.stopped.wait(self.comp.checkInterval)
            else:
                checkHost()
                self.stopped.wait(HOST_CHECKINTERVAL)

    def stop(self):
        self.stopped.set()