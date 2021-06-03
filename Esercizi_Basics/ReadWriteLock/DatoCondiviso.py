from threading import Lock,Condition

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
