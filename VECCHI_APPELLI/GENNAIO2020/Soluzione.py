from threading import Thread,Condition,RLock
from time import sleep
from random import random,randint 

class RoundRobinLock:

    SOGLIASTARVATION = 5

    def __init__(self,N : int):
        self.nturni = N
        self.lock = RLock()
        self.conditions = [Condition(self.lock) for _ in range(0,N)]
        self.inAttesa = [0 for _ in range(0,N)]
        self.turnoCorrente = 0
        self.possessori = 0
        
        self.consecutiveOwners = 0


    def acquire(self,id : int):
        with self.lock:
            self.inAttesa[id] += 1
            while( self.possessori > 0 and 
                   self.turnoCorrente != id or 
                   self.turnoCorrente == id and 
                   self.consecutiveOwners > self.SOGLIASTARVATION and
                   max(self.inAttesa) > 0  
                 ):
                self.conditions[id].wait()
            
            print("Acquisisce il lock " + str(id) + "\n")
            self.inAttesa[id] -= 1
            self.possessori += 1
            self.consecutiveOwners += 1
    
    def release(self,id : int):
        with self.lock:
            self.possessori -= 1
            if self.possessori == 0:
                for i in range(1,self.nturni):
                    turno = (id + i) % self.nturni
                    if self.inAttesa[turno] > 0:
                        self.turnoCorrente = turno
                        self.consecutiveOwners = 0
                        print("Rilascia il lock " + str(id) + "\n")
                        print("Si prepara ad acquisire il lock " + str(turno) + "\n")
                        self.conditions[turno].notifyAll()
                        break


class Animale(Thread):

    def __init__(self,id: int, idTurno : int, R : RoundRobinLock):
        super().__init__()
        self.idTurno = idTurno
        self.iterazioni = 1000
        self.lock = R

    def run(self):
        while(self.iterazioni > 0):
                self.iterazioni -= 1
                self.lock.acquire(self.idTurno)
                #self.lock.__print__()
                self.lock.release(self.idTurno)

NGruppi = 5        

R = RoundRobinLock(NGruppi)
for i in range(0,60):
    Animale(i,randint(0,NGruppi-1),R).start()
    
