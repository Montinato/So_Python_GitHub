from threading import Lock

class Bacchetta:
    def __init__(self):
        self.lock = Lock()

    def prendiBacchetta(self):
        self.lock.acquire()

    def lasciaBacchetta(self):
        self.lock.release()