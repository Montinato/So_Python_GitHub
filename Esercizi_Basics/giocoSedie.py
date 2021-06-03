from threading import Thread,Lock
from time import sleep
from random import random,randrange

# STRUTTURA DATI
class Posto:

    def __init__(self):
        self.occupato = False
        self.lock = Lock()

    def libero(self):
        return not self.occupato
    
    def occupato(self,v):
        self.occupato = v 

    def testaEoccupa(self):
        with self.lock:
            if self.occupato:
                return False 
            else:
                self.occupato = True
                return True 

# THREAD 
class Partecipante(Thread):

    def __init__(self,posti):
        super().__init__()
        self.posti = posti 

    def run(self):
        sleep(randrange(5))
        for i in range(0,len(self.posti)):
            if self.posti[i].testaEoccupa():
                print("Sono il Thread %s. Occupo il posto %d" % (self.getName(),i))
                return 
        print("Sono il Thread %s. HO PERSO", % (self.getName(),i))
        return

# CLASSE DISPLAY DI SUPPORTO PER DELLE STAMPE DI DEBUG 
class Display(Thread):
    
    def __init__(self,posti):
        super().__init__()
        self.posti = posti

    def run(self):
        while(True):
            sleep(1)
            for i in range(0,len(self.posti)):
                if(self.posti[i].libero()):
                    print("-",end='',flush=True)
                else:
                    print("o",end='',flush=True)
            print('')                

# MAIN

NSEDIE = 10 

posti = [ Posto() for i in range (0,NSEDIE)]

display = Display(posti)
display.start() 

for k in range(0,NSEDIE+1):
    k = Partecipante(posti)
    k.start()

# Non mi funziona per bene il display e le stampe senza il Display non compaiono 

# ERA UN PROBLEMA DI INDENTAZIONE 