from threading import Thread,RLock,Condition
from random import random
from time import sleep

#
# Funzione di stampa sincronizzata
#
plock = RLock()
def prints(s):
    plock.acquire()
    print(s)
    plock.release()

class DatoCondiviso():

    def __init__(self,v):
        self.dato = v
        self.numLettori = 0
        self.ceUnoScrittore = False
        self.lock = RLock()
        self.condition = Condition(self.lock)

        # Qui salvo lettori e scrittori
        self.accessi = []

        # Provo ad impostare il codice usando 2 condition distinte
        self.conditionScrittori = Condition(self.lock)
        self.conditionLettori = Condition(self.lock)

    def getDato(self):
        return self.dato
    
    def setDato(self, i):
        self.dato = i

    def acquireReadLock(self,tipo : int):
        self.lock.acquire()
        while self.ceUnoScrittore:
            self.conditionLettori.wait()
        self.accessi.insert(0,tipo)
        self.numLettori += 1
        self.lock.release()

    def releaseReadLock(self, tipo : int):
        self.lock.acquire()
        self.numLettori -= 1
        if self.numLettori == 0:
            self.conditionScrittori.notify()
        self.accessi.remove(tipo)
        self.lock.release()

    def acquireWriteLock(self, tipo : int):
        self.lock.acquire()
        while self.numLettori > 0 or self.ceUnoScrittore:
            self.conditionScrittori.wait()
        self.accessi.insert(0,tipo)
        self.ceUnoScrittore = True
        self.accessi.insert(0,tipo)
        self.lock.release()

    def releaseWriteLock(self, tipo : int):
        self.lock.acquire()
        self.ceUnoScrittore = False
        self.conditionLettori.notify_all()
        self.accessi.remove(tipo)
        self.lock.release()

    def acquireTLock(self,tipo : int):
        with self.lock:
            while( self.numLettori > 3 and ( accessi[0] == 1 and  accessi[1] == 1)):
                self.conditionScrittori.wait()
                self.conditionLettori.wait()
            self.accessi.insert(0,tipo)
            
    def releaseTLock(self,tipo : int ):
        with self.lock:
            self.conditionScrittori.notifyAll()
            self.accessi.remove(tipo)


class Scrittore(Thread):
    
    maxIterations = 10

    def __init__(self, i, dc):
        super().__init__()
        self.id = i
        self.dc = dc
        self.iterations = 0
        
        # Aggiungo per identificare gli scrittori
        self.tipo = 1

    def run(self):
        while self.iterations < self.maxIterations:
            prints("Lo scrittore %d chiede di scrivere." % self.id)
            self.dc.acquireWriteLock(self.tipo)
            prints("Lo scrittore %d comincia a scrivere." % self.id )
            sleep(random())
            self.dc.setDato(self.id)
            prints("Lo scrittore %d ha scritto." % self.id)
            self.dc.releaseWriteLock(self.tipo)
            prints("Lo scrittore %d termina di scrivere." % self.id)
            sleep(random() * 5)
            self.iterations += 1

            if(self.iterations == 8):
                prints("Lo scrittore %d chiama acquireTLock()" % self.id)
                self.dc.acquireTLock(self.tipo)
                sleep(random())
                self.dc.releaseTLock(self.tipo)
                prints("Lo scrittore %d termina di scrivere." % self.id)



class Lettore(Thread):
    maxIterations = 10

    def __init__(self, i, dc):
        super().__init__()
        self.id = i
        self.dc = dc
        self.iterations = 0
        
        # Aggiungo per identificare i lettori
        self.tipo = 0

    def run(self):
        while self.iterations < self.maxIterations:
            prints("Il lettore %d Chiede di leggere." % self.id)
            self.dc.acquireReadLock(self.tipo)
            prints("Il lettore %d Comincia a leggere." % self.id)
            sleep(random())
            prints("Il lettore %d legge." % self.dc.getDato())
            self.dc.releaseReadLock(self.tipo)
            prints("Il lettore %d termina di leggere." % self.id)
            sleep(random() * 5)
            self.iterations += 1

            if(self.iterations == 8):
                prints("Il lettore %d chiama acquireTLock()" % self.id)
                self.dc.acquireTLock(self.tipo)
                sleep(random())
                self.dc.releaseTLock(self.tipo)
                prints("Il lettore %d termina di scrivere, releaseTLock()." % self.id)
  

if __name__ == '__main__':
        dc = DatoCondiviso(999)

        NUMS = 5
        NUML = 5
        scrittori = [Scrittore(i,dc) for i in range(NUMS)]
        lettori = [Lettore(i,dc) for i in range(NUML)]
        for s in scrittori:
            s.start()
        for l in lettori:
            l.start()


