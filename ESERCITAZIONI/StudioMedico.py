from threading import Thread,RLock,Condition
from time import sleep
from random import randint,random
from queue import Queue

# IMPLEMENTAZIONE IANNI 

class SalaDiAttesa:

    def __init__(self):             # OK 
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.codaPazientiVisita = Queue(10)
        self.codaPazientiRicetta = Queue(10)
        self.codaPazientiRicettaPrioritaria = Queue(10)
        

    def aggiungiPazienteVisita(self,p):     # OK 
        self.codaPazientiVisita.put(p)
        p.ricetta.attendiRicetta()
        return p.ricetta

    def aggiungiPazienteRicetta(self,p):    #  OK
        self.codaPazientiRicetta.put(p)
        self.lock.acquire()
        self.condition.notifyAll()
        self.lock.release()
        p.ricetta.attendiRicetta()
        return p.ricetta

    def aggiungiPazienteRicettaPrioritaria(self,p):     # OK
        self.codaPazientiRicettaPrioritaria.put(p)
        self.lock.acquire()
        self.condition.notifyAll()
        self.lock.release()
        p.ricetta.attendiRicetta()
        return p.ricetta

    def getPazienteVisita(self):    # OK
        return self.codaPazientiVisita.get()

    def getProssimoPazienteRicetta(self):   # OK 
        with self.lock:
            while self.codaPazientiRicettaPrioritaria.empty() and self.codaPazientiRicetta.empty():
                self.condition.wait()

            if(not self.codaPazientiRicettaPrioritaria.empty()):
                return self.codaPazientiRicettaPrioritaria.get()
            else:
                return self.codaPazientiRicetta.get()


class Medico(Thread):           # OK
    def __init__(self,salaDiAttesa):    # OK
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):  #   OK
        while True:
            p = self.salaDiAttesa.getPazienteVisita()
            n = random()

            sleep(randint(1,4))

            if(n > 0.66666):
                p.ricetta.medicina="TUTTO OK"
                p.ricetta.ricettaPronta()
            elif(n > 0.3333):
                p.ricetta.medicina = "STAI BENE, PUOI ANDARE VIA SENZA RICETTA"
                p.ricetta.ricettaPronta()
            else:
                self.salaDiAttesa.aggiungiPazienteRicettaPrioritaria(p)

class Segretaria(Thread):       # OK 
    
    def __init__(self,salaDiAttesa):    # OK 
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):  # OK 
        while True:
            p = self.salaDiAttesa.getProssimoPazienteRicetta()
            n = random()

            sleep(randint(1,4))

            if (n>0.6666):
                p.ricetta.medicina="MAALOX"
            elif(n>0.3333):
                p.ricetta.medicina="OKI"
            else:
                p.ricetta.medicina = "AULIN"

            p.ricetta.ricettaPronta()

class Paziente:     # OK
    nextIdPaziente = 0

    def __init__(self):
        self.nome="Paziente_"+str(Paziente.nextIdPaziente)
        self.ricetta = Ricetta()
        Paziente.nextIdPaziente+=1          

class PazienteRun(Thread):      # OK 

    def __init__(self,salaAttesa):      # OK 
        super().__init__()
        self.salaAttesa = salaAttesa

    def run(self):              # OK 
        paziente = Paziente()

        n = random()

        if(n>0.5):
            self.salaAttesa.aggiungiPazienteVisita(paziente)
        else:
            self.salaAttesa.aggiungiPazienteRicetta(paziente)

        print("Il paziente " + paziente.nome + " e' uscito con la ricetta " + paziente.ricetta.medicina)

class GeneraPazienti(Thread):
    def __init__(self,salaAttesa):
        super().__init__()
        self.salaAttesa = salaAttesa

    def run(self):
        while True:
            pazienteRun = PazienteRun(self.salaAttesa)
            pazienteRun.start()


class Ricetta:

    #def __init__(self):
    lockRicetta = RLock()
    conditionRicetta = Condition(lockRicetta)
    medicina = None

    def attendiRicetta(self):
        self.lockRicetta.acquire()
        while self.medicina == None:
            self.conditionRicetta.wait()
        self.lockRicetta.release()

    def ricettaPronta(self):
        with self.lockRicetta:
            self.conditionRicetta.notifyAll()



def main():
    salaAttesa = SalaDiAttesa()
    m = Medico(salaAttesa)
    s1 = Segretaria(salaAttesa)
    s2 = Segretaria(salaAttesa)
    gp = GeneraPazienti(salaAttesa)

    m.start()
    s1.start()
    s2.start()
    gp.start()

if __name__ == "__main__":
    main()

        
