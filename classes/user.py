# The User Class for serverthread Tracking

import time

class User():
    def __init__(self, hwid, address):
        
        self.hwid = hwid
        self.address = address
        self.pos = (0,0)
        self.color = (0,0,0)
        self.name = hwid

        # Log In Variables
        self.logged_in = True
        self.last_update = time.time()
        self.last_log = time.time()

    # This function will return the info that gets
    # sent to clients. (Might get updated)
    def info(self):
        return {"pos": self.pos, "color": self.color, "name": self.name}
    
    def update(self, pos, color, newcon):
        self.last_update = time.time()
        self.pos = pos
        self.color = color

        if newcon:
            self.last_log = time.time()

    
