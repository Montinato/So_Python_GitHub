from threading import Thread,RLock,Condition
from random import randint
from queue import deque
from time import sleep

class Transazione:
    def __init__(self,A,B,V):
        self.A = A
        self.B = B
        self.V = V
    def GetSorgente(self):
        return self.A
    def GetDestinazione(self):
        return self.B
    def GetValore(self):
        return self.V

class ContoBancario:
    def __init__(self,s,t,id):
        self.RLock = RLock()
        self.hash = {id : s}        # Assegno il saldo s al conto con id -> id
        self.t = t                  # Lista delle transazioni

    def getSaldo(self):
        k = list(self.hash.values())        # Assegno ad una variabile la lista contenenti i valori dell'hashMap
        return k[0]

    def getId(self):
        x = list(self.hash.keys())      # Assegno ad una variabile la lista contenente le chiavi dell'hashMap
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
            saldo = self.getSaldo()+V
            self.hash = { A : saldo }

    def diminuisciSaldo(self,A,V):
        with self.RLock:
            if A==self.getId():
                saldo = self.getSaldo() - V 
                self.hash={ A : saldo }

class Banca:

    def __init__(self,conti):
        self.conti = conti
        self.RLock = RLock()

    def getSaldo(self,C):
        with self.RLock:
            return self.conti.get(C).getSaldo()

    def getConti(self):
        return self.conti.keys()

    def trasferisci(self,A,B,N):
        with self.RLock:
            t = Transazione(A,B,N)

            if self.conti.get(A).getSaldo() < N:
                return False
            else:
                self.conti.get(B).aumentaSaldo(B,N)
                self.conti.get(A).diminuisciSaldo(A,N)
                self.conti.get(A).addTransaction(t,A)
                self.conti.get(B).addTransaction(t,B)
                print("Il saldo di %s e': %d il saldo di %s e' :%d" %   (A,self.getSaldo(A),B,self.getSaldo(B)))
                return True
                
class Cliente(Thread):

    def __init__(self,banca):
        self.banca = banca
        super().__init__()

    def run(self):
        while True:
            arr = list(self.banca.getConti())
            pos1 = randint(0,len(arr)-1)
            pos2 = randint(0,len(arr)-1)

            if pos1 != pos2:
                v = randint(10,1000)
                if self.banca.trasferisci(arr[pos1],arr[pos2],v) == False:
                    print("Non e' stato possibile trasferire i soldi dal conto %s al conto %s" % (arr[pos1],arr[pos2]))
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

