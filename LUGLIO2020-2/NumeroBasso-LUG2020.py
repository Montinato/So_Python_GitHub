from threading import Thread, RLock, Condition, current_thread
from random import randint

class Player(Thread):
    
    def __init__(self,nb):
        super().__init__()
        self.nb = nb

    def run(self):
        self.nb.puntaNumero(randint(1,10))

class NumeroBasso:
       

    def __init__(self):
        self.giocate = []
        self.lock = RLock()
        self.threadGioca = Condition(self.lock)
        self.partitaInCorso = False
        self.nGiocate = 0
        self.barrier = None

    def gioca(self,N : int) -> int:
        with self.lock:
            self.giocate = {}
            self.nGiocate = 0
            self.partitaInCorso = True
            for _ in range(0,N):
                Player(self).start()
            while(self.nGiocate < N):
                self.threadGioca.wait()
            self.partitaInCorso = False
            for k in sorted(self.giocate):
                if len(self.giocate[k]) == 1:
                    return self.giocate[k][0]
            
            return 0
 
    def puntaNumero(self,n : int):
        with self.lock:
            self.giocate.setdefault(n,[]).append(current_thread().ident)
            self.nGiocate += 1
            self.threadGioca.notify()

if __name__ == '__main__':
    gameManager = NumeroBasso()

    v = 1
    while v != 0:
        v = gameManager.gioca(10)