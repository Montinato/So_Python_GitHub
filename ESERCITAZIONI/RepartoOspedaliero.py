from threading import Thread,Condition,RLock
from random import random,randint
from time import sleep
from queue import Queue

class Stanza:
    def __init__(self):
        self.medico = False

        self.visitatori = []
        self.medici = []

        self.lock = RLock()

        self.conditionMedico = Condition(self.lock)
        self.conditionVisitatori = Condition(self.lock)

    def entraMedico(self,name):
        
        with self.lock:
            print("\n")
            while  len(self.visitatori) > 0 or len(self.medici) > 0:
                self.conditionMedico.wait()

            self.medici.append(name)
            #self.medico = True
            print("entraMedico() = " + " Il medico " + name + " entra nella stanza se non ci sono visitatori.")
            print("\n")

    def esceMedico(self,name):

        with self.lock:
            print("\n")
            print("esceMedico() = " + " Il medico " + name + " finisce la visita ed esce dalla stanza.")
            self.medici.remove(name)
            self.conditionMedico.notifyAll()
            self.conditionVisitatori.notifyAll()
            print("\n")


    def entraVisitatore(self,name):
        with self.lock:
            print("\n")
            print("entraVisitatore() = "+ " Il visitatore " + name + " non puo' entrare perche' il medico sta visitando")
            while( len(self.medici) > 0 and len(self.visitatori) == 5 ):
                self.conditionVisitatori.wait()
            
            print("entraVisitatore() = " + " Il visitatore " + name + " puo' finalmente entrare, il medico ha finito la visita!")
            self.visitatori.append(name)
            print("\n")

    def esceVisitatore(self,name):
        with self.lock:
            print("\n")
            print("esceVisitatore() = " + " Il visitatore" + name +" termina la visita e se ne va a casa! ")
            self.visitatori.remove(name)
            if len(self.visitatori) == 0:
                self.conditionMedico.notifyAll()
            print("esceVisitatore() = " + " Un medico si prepara ad entrare")
            print("\n")

class Visitatore(Thread):
    def __init__(self,stanza,name):
        super().__init__()
        self.stanza = stanza
        self.name = name

        
    def run(self):
        while True:
            x = randint(10,100)
            self.stanza.entraVisitatore(self.name)         
            sleep(2)
            self.stanza.esceVisitatore(self.name)

class Medico(Thread):
    def __init__(self,stanza,name):
        super().__init__()
        self.stanza = stanza
        self.name = name

    def run(self):
        while True:
            self.stanza.entraMedico(self.name)          
            sleep(2)
            self.stanza.esceMedico(self.name)


stanza = Stanza()


print("START")


for i in range(6):
    medico = Medico(stanza,"Medico-%s" % i)
    medico.start()
    
for i in range (10):
    amico = Visitatore(stanza,"Amico-%s" % i)
    amico.start()



# IL PROGRAMMA FUNZIONA DEVO RISOLVERE LA STARVATION 

# UNA VOLTA RISOLTO SISTEMARE IL PROBLEMA DEL BARBIERE VELOCEMENTE