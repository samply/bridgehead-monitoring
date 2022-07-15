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
        if isinstance(self.comp, Service):
            self.service_thread()
        else:
            self.host_thread()

    def host_thread(self):
        while not self.stopped.isSet():
            checkHost()
            self.stopped.wait(HOST_CHECKINTERVAL)

    def service_thread(self):
        while not self.stopped.isSet():
            checkService(self.comp)
            self.stopped.wait(self.comp.checkInterval)
        
    def stop(self):
        self.stopped.set()