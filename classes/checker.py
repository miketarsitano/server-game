# Checker thread for the server to manage 
# server-based inputs/outputs 

import time
import threading

class CheckerThread(threading.Thread):

    def __init__(self, name='checker-thread'):

        super(CheckerThread, self).__init__(name=name)
        self.start()

    def run(self):
        
        while True:
            time.sleep(10)