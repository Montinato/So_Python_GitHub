from threading import Thread,Lock
from random import randint,random,randrange
import time 
from DatoCondiviso import DatoCondiviso

plock = Lock()
def prints(s):
        plock.acquire()
        print(s)
        plock.release()

class Lettore(Thread):

    maxIterations = 100

    def __init__(self,i,dc):
        super().__init__() 
        self.id = i 
        self.dc = dc  
        self.iterations = 0

    def run(self):
        while self.iterations < self.maxIterations:

            prints("Il lettore %d chiede di leggere. " % self.id)
            self.dc.acquireReadLock()

            prints("Il lettore %d comincia a leggere. " % self.id)
            time.sleep(random())
            prints("Il lettore %d ha scritto" % self.id )
            
            self.dc.releaseReadLock()
            
            prints("Il lettore %d termina di leggere. " % self.id )
            time.sleep(random() * 5 )
            self.iterations += 1
