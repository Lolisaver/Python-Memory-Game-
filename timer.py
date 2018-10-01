import time

class Timer:
    def __init__(self):
        self.startTime = time.time()

    def get(self):
        return time.time()-self.startTime
    
    def reset(self):
        self.startTime = time.time()