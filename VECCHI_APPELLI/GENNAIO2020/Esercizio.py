from threading import Thread,Condition,Lock
from time import sleep
from random import random,randint 

class RoundRobinLock:

    def __init__(self,N : int):
        self.ngruppi = N
        self.lock = Lock()
        self.condition = Condition(self.lock)

        self.maxSize = 18  
        self.giocatori = []

    def acquire(self,id : int):
        with self.lock:
            while( len(self.giocatori) == self.maxSize and self.giocatori[len(self.giocatori)-1] != id): 
                self.condition.wait()
            self.giocatori.append(id)
            print("Aggiungo ai giocatori " + str(id) + "\n")
            #self.condition.notify()

    def release(self,id : int):
        with self.lock:
            while( len(self.giocatori)>1 and self.giocatori[len(self.giocatori)-1] != id or self.giocatori[len(self.giocatori)-1]+1  != id ):
                print("Prova a rilasciare %d ma non ci riesco, vado in WAIT \n" % id)
                self.condition.wait()
            self.condition.notifyAll()
            print("Rimuovo dai giocatori " + str(id) + "\n")
            self.giocatori.remove(x)


class Player(Thread):

    def __init__(self,rr,id):
        super().__init__()
        self.id = id
        self.roundRLock = rr
        self.gioca = True

    def run(self):
        while(self.gioca):
            print("Il Player %d prova ad effettuare un acquire" % self.id )
            self.roundRLock.acquire(self.id)
            sleep(2)
            print("Il Player %d prova ed effettuare una release" % self.id )
            self.roundRLock.release(self.id)


            x = randint(1,1000)
            if(x == 1000):
                print(str(x))
                self.gioca = False
                break


if __name__ == "__main__":
    rrL = RoundRobinLock(10)

    for i in range(50):
        x = randint(1,10)
        Player(rrL,x).start()


# E' SBAGLIATO , GUARDA LA SOLUZIONE 
    

    