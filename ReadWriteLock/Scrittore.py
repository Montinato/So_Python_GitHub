from threading import Thread, Lock
from random import randint,random,randrange
import time
from DatoCondiviso import DatoCondiviso

plock = Lock()
def prints(s):
        plock.acquire()
        print(s)
        plock.release()

class Scrittore(Thread):

    maxIterations = 1000

    def __init__(self,i,dc):
        super().__init__() 
        self.id = i 
        self.dc = dc  
        self.iterations = 0

    def run(self):
        while self.iterations < self.maxIterations:

            prints("Lo scrittore %d chiede di scrivere. " % self.id)
            self.dc.acquireWriteLock()

            prints("Lo scrittore %d comincia a scrivere. " % self.id)
            time.sleep(random())
            self.dc.setDato(self.id)
            prints("Lo scrittore %d ha scritto" % self.id )
            
            self.dc.releaseWriteLock()

            prints("Lo scrittore %d termina di scrivere. " % self.id )
            time.sleep(random() * 5 )
            self.iterations += 1
