from threading import Thread, Event
from check_service import checkService

class MyThread(Thread):
    def __init__(self, comp=""):
        Thread.__init__(self)
        self.stopped = Event()
        self.comp = comp

    def run(self):                    
        while not self.stopped.isSet():
            checkService(self.comp)
            self.stopped.wait(self.comp.checkInterval)

    def stop(self):
        self.stopped.set()