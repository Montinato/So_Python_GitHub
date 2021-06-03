from threading import Thread,Lock,Condition
from queue import Queue 
from random import random,randint
from time import time,sleep

class SalaDiAttesa:

    def __init__(self):
        self.codaVisita = Queue(10)
        self.codaRicetta = Queue(10)
        self.codaRicettaPrioritaria = Queue(10)
        self.lock = Lock()
        self.condition = Condition(Lock)
        self.conditionPrioritaria = Condition(Lock)

    def nextPaziente(self,paziente):
        return paziente


    def visitaMedica(self,paziente):
        with self.lock:
            while ( len(self.codaVisita) == 10 ):
                self.condition.wait() 

                self.codaVisita.put(paziente)

                value = randint(1,10) 

                sleep(value)

                if value > 5:
                    self.codaRicetta.put(paziente)

                self.condition.notifyAll()

    def ricettaMedica(self,paziente):
        with self.lock:
            while ( len(self.codaRicetta) == 10):
                self.condition.wait()

                self.codaRicetta.put(paziente)

                sleep(randint(1,8))

                self.condition.notifyAll()


    

    
class Medico(Thread):
    
    def __init__(self,salaDiAttesa):
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):
        while True:
            print("Il Medico %s arriva e timbra il cartellino " % Medico.getName())

            sleep(randint(1,10))

            print("Il Medico %s e' pronto a visitare i pazienti " % Medico.getName())

            paziente = self.salaDiAttesa.nextPaziente()

            print("Il Medico %s visita il paziente %d  " % self.getName(), paziente.getName())

            self.salaDiAttesa.visitaMedica(paziente)


class Segretaria(Thread):
   
    def __init__(self,salaDiAttesa):
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):
        pass

class Paziente(Thread):

    def __init__(self,salaDiAttesa,tipoVisita):
        super().__init__()
        self.salaDiAttesa = SalaDiAttesa()
        self.azione = azione
        self.tipoVisita = tipoVisita

    def run(self):
        while True: 
            print("Il Paziente %s entra in sala di attesa" % Paziente.getName())
            self.azione = randint(1,2)

            
            print("Il Paziente %s e' in attesa  " % Paziente.getName())

            
            # Il paziente aspetta il proprio turno 
            sleep(randint(self.azione*5))


            self.salaDiAttesa.nextPaziente(Paziente())

            

            # DEVO COMPLETARE E VEDERE PER BENE COME STRUTTURARE IL PROGRAMMA 