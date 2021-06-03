from threading import Thread,Lock
from random import randrange
from Tavolo import Tavolo
import time, random
from time import sleep

class Filosofo(Thread):
    
    def __init__(self,tavolo,pos):
        super().__init__()
        self.posizione = pos
        self.t = tavolo
        self.name = "Philip %s" % pos

    def attesaCasuale(self,msec):
        sleep(randrange(msec)/1000.0)

    def pensa(self):
        print(f"Il filosofo { self.getName()} pensa." )
        self.attesaCasuale(1000)
        #sleep(2)
        print(f"Il filosofo { self.getName()} smette di pensare." )
    
    def mangia(self):
        
        print(f"Il filosofo {self.getName()} vuole mangiare.")

        # Acquire di entrambe le bacchette
        self.t.prendiLockSimultaneo(self.posizione)
        print(f"Il filosofo {self.getName()} ha le sue bacchette e mangia.")

        self.attesaCasuale(1)

        # Release di entrambe le bacchette
        print(f"Il filosofo {self.getName()} sta per lasciare le sue bacchette.")
        self.t.mollaLockSimultaneo(self.posizione)
        
        print(f"Il filosofo {self.getName()} termina di mangiare.")

    def run(self):
        while True:
            self.pensa()
            self.mangia()


tavolo = Tavolo()

filosofi = [ Filosofo(tavolo,i) for i in range(5) ]

for f in filosofi:
    f.start()
time.sleep(10)


