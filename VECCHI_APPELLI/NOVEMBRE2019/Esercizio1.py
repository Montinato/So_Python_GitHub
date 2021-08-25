from threading import Thread,RLock,Condition
from time import sleep
from random import randint,random
from queue import Queue

class PivotBlockingQueue:
    
    def __init__(self,N):
        self.N = N
        self.queue = []
        self.lock = RLock()
        self.conditionVuoto = Condition(self.lock)
        self.conditionPieno = Condition(self.lock)
        self.minMax = False   # False = min , True = max
        
        self.sogliaStarvation = 5

    def take(self):
        with self.lock:
            while(len(self.queue) == 2):
                print("Take e' in WAITTTTTT\n")
                self.conditionVuoto.wait()
            elem = self.setCriterioPivot(self.minMax)
            sleep(2)
            #print("L'elemento " + str(1) +" che verra' rimosso e' " % elem + "\n")
            self.queue.remove(elem)
            #print("L'elemento " + str(2) + " che verra' rimosso e' " % self.queue[len(self.queue)-1] + "\n")
            self.queue.pop()
            print("Ho rimosso gli elementi con la Take! \n" + "Nella queue ci sono : " + str(len(self.queue)) +" elementi\n" )
            self.conditionPieno.notifyAll()
            

    def put(self,T : int):
        with self.lock:
            while(len(self.queue) == self.N):
                self.conditionPieno.wait()
            print("Inserisco %d nella queue." % T)
            self.queue.append(T)
            self.conditionVuoto.notifyAll()

    def setCriterioPivot(self,minMax : bool):
        with self.lock:
            #print("Faccio conditionVuoto.notifyAll() \n")
            #self.conditionVuoto.notifyAll()
            #self.conditionPieno.notifyAll()
            
            x = randint(0,5)
            if x > 3:
                print("minMax = TRUE \n")
                self.minMax = True
            else:
                print("minMax = FALSE \n")
                self.minMax = False

            if(self.minMax):
                return max(self.queue)
            else:
                return min(self.queue)


class Player(Thread):

    def __init__(self,id,pivotBQ):
        super().__init__()
        self.id = id
        self.pivotBQ = pivotBQ

    def run(self):
        sleep(1)
        print("Player %d prova ad effettuare una put " % self.id + "\n")
        self.pivotBQ.put(self.id)
        sleep(1)
        print("Player %d prova ad effettuare una take " % self.id + "\n")
        self.pivotBQ.take()





if __name__ == "__main__":
    pivot = PivotBlockingQueue(50)

    for i in range(0,150):
        Player(i,pivot).start()
