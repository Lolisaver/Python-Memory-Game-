import time

class timer:
    def __init__(self):
        self.startTime = time.time()

    def getTime(self):
        return time.time()-self.startTime
    
    def reset(self):
        self.startTime = time.time()