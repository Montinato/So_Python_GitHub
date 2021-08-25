from threading import RLock,Thread,Condition
from random import Random,randint
from time import sleep


class Transazione:
  

    def __init__(self,sorgente,destinatario,valore):
        self.sorgente = sorgente
        self.destinatario = destinatario 
        self.valore = valore
    

    def getDestinazione(self):
        return self.destinatario

    def getSorgente(self):
        return self.sorgente

    def getValore(self):
        return self.valore



class ContoBancario:

    def __init__(self,s,t,id):
        self.RLock = RLock()
        self.hash = {id : s}    # Assegno il saldo s al conto id -> id
        self.t = t              # Lista delle transazioni

    def getSaldo(self):
        k = list(self.hash.values())
        return k[0]

    def getId(self):
        x = list(self.hash.keys())
        return x[0]

    def addTransaction(self,tr,id):
        with self.RLock:
            if id != self.getId():
                return
            if len(self.t) < 50:
                self.t.insert(0,tr)
            else:
                self.t.pop()
                self.t.insert(0,tr)

    def aumentaSaldo(self,A,V):
        with self.RLock:
            saldo = self.getSaldo() + V 
            self.hash = { A : saldo}

    def diminuisciSaldo(self,A,V):
        with self.RLock:
            if A == self.getId():
                saldo = self.getSaldo() - V 
                self.hash = { A : saldo}

    


class Banca:

    def __init__(self,conti):
        self.conti = conti
        self.RLock = RLock()
        self.condition = Condition(self.RLock)

    def getSaldo(self,C):
        with self.RLock:
            return self.conti.get(C).getSaldo()
            self.condition.notifyAll()

    def getConti(self):
        return self.conti.keys()

    def trasferisci(self,A,B,N):
        with self.RLock:

            t = Transazione(A,B,N)

            self.conti.get(B).aumentaSaldo(B,N)
            self.conti.get(A).diminuisciSaldo(A,N)
            self.conti.get(A).addTransaction(t,A)
            self.conti.get(A).addTransaction(t,B)

            print("         INIZIO TRANSAZIONE")
            print("         %s ha trasferito %s euro sul conto di %s" % (A,N,B))
            print("         FINE TRANSAZIONE")
            print("\n")
            # print("Il saldo di %s e': %d il saldo di %s e' %d" % (A,self.getSaldo(A),B,self.getSaldo(B)))

    def checkSaldo(self,A,B,N):
        with self.RLock:
            while self.conti.get(A).getSaldo() < N:
                self.condition.wait()
            #self.condition.notifyAll()

    def show(self,A,B):
       print( "         Il saldo di %s e': %d il saldo di %s e' :%d" %   (A,self.getSaldo(A),B,self.getSaldo(B)))




            

class Cliente(Thread):

    def __init__(self,banca):
        super().__init__()
        self.banca = banca

    def run(self):
        while True:
            arr = list(self.banca.getConti())      
            pos1 = randint(0,len(arr)-1)
            pos2 = randint(0,len(arr)-1)

            if pos1 != pos2:
                v = randint(10,1000)

                #self.banca.checkSaldo(arr[pos1],arr[pos2],v)
                #print("ABBIAMO UN GROSSO PROBLEMA")

                self.banca.trasferisci(arr[pos1],arr[pos2],v)
                self.banca.show(arr[pos1],arr[pos2])
                sleep(1)
def main():

    t1 = list() 
    
    t2 = list() 
    
    t3 = list() 
    
    t4 = list()

    c1 = ContoBancario(10000,t1,'A')
    
    c2 = ContoBancario(10000,t2,'B')
    
    c3 = ContoBancario(10000,t3,'C')
    
    c4 = ContoBancario(10000,t4,'D') 

    conti = { 'A':c1,'B':c2,'C':c3,'D':c4 }

    banca = Banca(conti)

    clienti = [ Cliente(banca) for x in range(10)]

    for i in clienti:
        i.start()

 

if __name__=="__main__":
    main()

