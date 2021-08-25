from threading import Thread,RLock,Condition
from time import sleep
from random import random,randint 


class FairLock():

    def __init__(self):
         
        self.array = []
        self.rLock = RLock()
        self.condition = Condition(self.rLock)
        self.conditionUrgente = Condition(self.rLock)
        self.numeroUAcquire = 1
        

        self.MAX = 10

    def acquire(self,p):
        with self.rLock: 
            while(len(self.array) == self.MAX):
                self.condition.wait()
            print("ACQUIRE : Ho aggiunto %d" %p.id + "\n")
            self.array.append(p)          

    def urgentAcquire(self,p):
        with self.rLock:
            while(self.numeroUAcquire == 0 or len(self.array) == self.MAX):
                self.conditionUrgente.wait()
            print("URGENT ACQUIRE : Ho aggiunto %d" % p.id + "\n")
            self.array.append(p)
            self.numeroUAcquire+=1

    def release(self,p):
        with self.rLock:
            while(len(self.array) == 0):
                self.condition.wait()
            print("RELEASE: \n")

            v = len(self.array)-1;
            print ("L'array ha " + str(v) + " elementi \n") 
            
            print("Priorita = " + str(self.array[v].priorita)+"\n")
            if(self.array[v].priorita == 1 and self.numeroUAcquire >0):
                print("RELEASE DI  URGENT ACQUIRE : rimuovo il giocatore %d \n" % self.array[v].id)
                self.array.remove(p)
                self.conditionUrgente.notifyAll()
                self.numeroUAcquire-=1
                self.condition.notifyAll()
            elif self.array[v].priorita == 0:
                print("RELEASE DI  ACQUIRE : rimuovo il giocatore %d \n" % self.array[v].id)
                self.array.remove(p)
                self.condition.notifyAll()

    def setStarvationControl(self,n):
        self.numeroUAcquire = n

class Player(Thread):

    id = 0
    def __init__(self,f,p):
        super().__init__()
        self.id = Player.id
        self.fairLock = f
        self.priorita = p
        Player.id+=1

    def run(self):
        while(self.id<100):
            x = randint(1,3)
            print("Player " + str(self.id) + " con priorita' "+ str(self.priorita) + "\n")

            sleep(2)

            if(x >= 2):
                sleep(0.5)
                self.fairLock.acquire(self)
            else:
                sleep(0.5)
                self.fairLock.urgentAcquire(self)

            
            self.fairLock.release(self)
            
if __name__ == '__main__':
    fairLock = FairLock()

    for i in range(0,10):
        x = randint(0,1)
        Player(fairLock,x).start()

