from threading import Thread, RLock, Condition, current_thread
from random import randint

class Player(Thread):
    
    def __init__(self,nb):
        super().__init__()
        self.nb = nb
        self.esito = False

    def run(self):
        print("Metodo puntaNumero() :\n")
        self.nb.puntaNumero(randint(1,10),self.esito)

class NumeroBasso:
       

    def __init__(self):
        self.giocate = []
        self.lock = RLock()
        self.threadGioca = Condition(self.lock)
        self.partitaInCorso = False
        self.nGiocate = 0
        self.barrier = None

        self.iterazioni = 0
        

    def gioca(self,N : int) -> int:
        with self.lock:
            print("Metodo gioca(): \n")
            self.giocate = {}
            self.nGiocate = 0
            self.partitaInCorso = True

            for _ in range(0,N):
                Player(self).start()

            while(self.nGiocate < N):
                self.threadGioca.wait()

    def puntaNumero(self,n : int,esito : bool):
        with self.lock:
            #print("Metodo puntaNumero() :\n")
            self.giocate.setdefault(n,[]).append(current_thread().ident)
            self.nGiocate += 1
            print("Stampa nGiocate : " + str(self.nGiocate) + "\n")
            
            if self.nGiocate == 10:
                for k in sorted(self.giocate):
                    if len(self.giocate[k]) == 1:
                        esito = True
                        
                        #self.threadGioca.wait()
                        print ( str(esito) + "WINNER" + str(self.giocate[k]) + "\n" )

            self.partitaInCorso = False
            self.threadGioca.notifyAll()
                
                

if __name__ == '__main__':
    gameManager = NumeroBasso()

    v = 1

    while v != 0:
        v = gameManager.gioca(10)