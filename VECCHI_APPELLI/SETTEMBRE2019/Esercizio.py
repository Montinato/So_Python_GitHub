from threading import Thread,RLock,Condition
from time import sleep
from random import random,randint

class Torre:

    def __init__(self):
        self.torre = []
        self.lock = RLock()
        self.conditionMattone = Condition(self.lock)
        self.conditionCemento = Condition(self.lock)

        self.numeroStrati = 0
        self.dimensione = 3

        self.contaMattoni = 0
        self.contaCemento = 0

        self.stratoMattoni = 0
        self.stratoCemento = 0

        self.stop = False

    def makeTorre(self,H : int,M : int,C : int):
        self.numeroStrati = H
            
        for x in range(0,C):
            Cementatore(x,self).start()

        for i in range(0,M):
            Mattonatore(i,self).start()

    def workMattone(self,id):
        with self.lock:
            sleep(2)
            while(self.contaMattoni == 3 or self.stratoCemento == 0  ):
                print("MATTONATORE IN WAITTTTTT \n")  
                self.conditionMattone.wait()


            if(self.stratoMattoni + self.stratoCemento == self.numeroStrati):
                self.prints(self.stratoMattoni,self.stratoCemento)
                
            self.contaMattoni += 1

            if(self.contaMattoni == self.dimensione):
                self.contaMattoni = 0
                self.stratoMattoni += 1
                print("Cementatore aggiunge %d \n" % id )
                self.torre.append(id)

            self.conditionCemento.notifyAll()

            print("MATTONATORE: \n")
            print("ContaMattoni = " + str(self.contaMattoni) + "\n")
            print("StratoMattoni = " + str(self.stratoMattoni) + "\n")
            print("NumeroStrati = " + str(self.numeroStrati) + "\n")
            print("\n")

            
            

    def workCemento(self,id):
        with self.lock:
            sleep(2)
            while(self.contaCemento == 3  ):
                print("CEMENTATORE IN WAITTTTTT \n")
                self.conditionCemento.wait()

            if(self.stratoMattoni + self.stratoCemento == self.numeroStrati):
                self.prints(self.stratoMattoni,self.stratoCemento)
                
            self.contaCemento += 1

            if(self.contaCemento == self.dimensione):
                self.contaCemento = 0
                self.stratoCemento += 1
                print("Cementatore aggiunge %d \n" % id )
                self.torre.append(id)

            self.conditionMattone.notifyAll()
            print("Adesso il mattonatore si deve svegliare! \n")

            print("CEMENTATORE: \n")
            print("ContaCemento = " + str(self.contaCemento) + "\n")
            print("StratoCemento = " + str(self.stratoCemento) + "\n")
            print("NumeroStrati = " + str(self.numeroStrati) + "\n")  
            print("\n")

    def prints(self,numMattoni,numCementi):
        with self.lock:
            for x in range(0,numMattoni + numCementi):
                if(x%2 == 0):
                    print("---\n");
                else:
                    print("***\n")

    

class Mattonatore(Thread):

    def __init__(self,id,torre):
        super().__init__()
        self.id = id
        self.torre = torre

    def run(self):
        print("Mattonatore %d prova a costruire" % self.id)
        self.torre.workMattone(self.id)


class Cementatore(Thread):

    def __init__(self,id,torre):
        super().__init__()
        self.id = id
        self.torre = torre

    def run(self):
        print("Cementatore %d prova a costruire" % self.id)
        self.torre.workCemento(self.id)



if __name__ == "__main__":

    torre = Torre()

    torre.makeTorre(6,10,10)
