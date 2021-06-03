from threading import Thread,Lock
from Tavolo import Tavolo
from random import randrange
from time import sleep, time

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
        #self.attesaCasuale(1000)
        #sleep(2)
        print(f"Il filosofo { self.getName()} smetti di pensare." )
    
    def mangia(self):
        
        print(f"Il filosofo {self.getName()} vuole mangiare.")
        self.t.bacchetta[self.posizione].prendiBacchetta()
        print(f"Il filosofo {self.getName()} ha preso la prima bacchetta.")
        self.t.bacchetta[(self.posizione+1) % 5].prendiBacchetta()
        print(f"Il filosofo {self.getName()} ha preso la seconda bacchetta e mangia.")

        #self.attesaCasuale(1000)
        #sleep(1)
        print(f"Il filosofo {self.getName()} termina di mangiare.")

        self.t.bacchetta[self.posizione].lasciaBacchetta()
        print(f"Il filosofo {self.getName()} ha lasciato la prima bacchetta.")
        self.t.bacchetta[(self.posizione+1) % 5].lasciaBacchetta()
        print(f"Il filosofo {self.getName()} ha preso la seconda bacchetta.")
    
    def run(self):
        while True:
            self.pensa()
            self.mangia()





tavolo = Tavolo()

filosofi = [ Filosofo(tavolo,i) for i in range(5) ]

for f in filosofi:
    f.start()


