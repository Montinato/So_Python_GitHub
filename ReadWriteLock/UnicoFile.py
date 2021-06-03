from threading import Lock,Condition,Thread
import time
from random import randint,random,randrange

plock = Lock()
def prints(s):
        plock.acquire()
        print(s)
        plock.release()

class DatoCondiviso:


    # Voglio una struttura dati alla quale posso accedere in Lettura oppure in Scrittura
    # Con un accesso diverso rispetto ai classici Lock e RLock

    def __init__(self,v):
        self.dato = v
        self.lockDiServizio = Lock()
        self.attesaWrite = Condition(self.lockDiServizio)
        self.attesaRead = Condition(self.lockDiServizio)
        self.numLettori = 0
        self.ciSonoLettori = False
        self.ciSonoScrittori = False 

    def getDato(self):
        return self.dato

    def setDato(self,v):
        self.dato = v 

    def acquireReadLock(self):
        
        with self.lockDiServizio:
            while ( self.ciSonoScrittori ):
                self.attesaRead.wait()
            #self.ciSonoLettori = True
            self.numLettori += 1

    def releaseReadLock(self):
        with self.lockDiServizio:
            self.attesaWrite.notifyAll()
            self.numLettori -= 1

    def acquireWriteLock(self):
        with self.lockDiServizio:
            # while ( not (not self.ciSonoScrittori and not self.ciSonoLettori) ) : EQUIVALENTE AL WHILE DI RIGA 38, SCRITTO IN MODO DIVERSO 
            while (  self.ciSonoScrittori or self.numLettori > 0 ):
                self.attesaWrite.wait()
            self.ciSonoScrittori = True

    def releaseWriteLock(self):
        with self.lockDiServizio:
            self.attesaRead.notifyAll()
            self.attesaWrite.notifyAll()
            self.ciSonoScrittori = False

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
            time.sleep(1)
            self.dc.setDato(self.id)
            prints("Lo scrittore %d ha scritto" % self.id )
            
            self.dc.releaseWriteLock()
            
            prints("Lo scrittore %d termina di scrivere. " % self.id )
            time.sleep(random() * 5 )
            self.iterations += 1

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
            time.sleep(1)
            prints("Il lettore %d ha scritto" % self.id )
            
            self.dc.releaseReadLock()
            
            prints("Il lettore %d termina di leggere. " % self.id )
            time.sleep(random() * 5 )
            self.iterations += 1




dc = DatoCondiviso(999)

NUMS = 5
NUML = 5 

scrittori = [ Scrittore(i,dc) for i in range(NUMS)]

lettori = [ Lettore(i,dc) for i in range(NUML)]

for s in scrittori:
    s.start()

for l in lettori:
    l.start()

time.sleep(1)

# DEVO TROVARE L'ERRORE

