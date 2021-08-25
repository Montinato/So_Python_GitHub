#!/usr/bin/env python

from threading import RLock, Condition, Thread
from time import sleep
from random import random, randint

debug = True

#
# Stampa sincronizzata
#
plock = RLock()
def sprint(s):
    with plock:
        print(s)
#
# Stampa solo in debug mode
#
def dprint(s):
    with plock:
        if debug:
            print(s)

class RunningSushiBuffer:
    
    theBuffer : list
    dim : int
    lock : RLock
    condition : Condition

    def __init__(self, dim):
        self.theBuffer = [None] * dim
        self.zeroPosition = 0
        self.dim = dim
        self.lock = RLock()
        self.condition = Condition(self.lock)

    def _getRealPosition(self,i : int):
        return (i + self.zeroPosition) % self.dim    

    def get(self, pos : int):
        with self.lock:
            while self.theBuffer[self._getRealPosition(pos)] == None:
                self.condition.wait()
            palluzza = self.theBuffer[self._getRealPosition(pos)]
            self.theBuffer[self._getRealPosition(pos)] = None
            return palluzza

    def put(self, t):
        with self.lock:
            while self.theBuffer[self._getRealPosition(0)] != None:
                self.condition.wait()
            self.theBuffer[self._getRealPosition(0)] = t

    def shift(self, j = 1):
        with self.lock:            
            # 
            #  uso zeroPosition per spostare la posizione 0 solo virtualmente, 
            #  anziche' dover ricopiare degli elementi
            # 
            self.zeroPosition = (self.zeroPosition + j) % self.dim
            # 
            #    E' solo grazie a uno shift che puo' crearsi la condizione per svegliare un thread
            #    in attesa, rispettivamente su put() o su get()
            # 
            self.condition.notifyAll()

    #
    #  Soluzione domanda Turno 1
    #
    def __checkFreePositions(self,n):
        for i in range(0,n):
            if self.theBuffer[self._getRealPosition(i)] != None:
                return False
        return True

    def putList(self,L):
        with self.lock:
            while(self.__checkFreePositions(len(L))):
                self.condition.wait()
            for elem in L:
                self.put(elem)
                self.shift()

    #
    # Soluzione domanda Turno 2
    #
    def __rawPut(self,T,i):
        self.theBuffer[self._getRealPosition(i)] = T

    def getList(self,N,t,i):
        with self.lock:
            retList = []
            elemDaPrendere = N
            while elemDaPrendere > 0:
                T = self.get(i)
                if T != t:
                    retList.append(T)
                    elemDaPrendere -= 1
                else:
                    self.__rawPut(T,i)
            return retList


class NastroRotante(Thread):
    
    def __init__(self, d : RunningSushiBuffer):
        super().__init__()
        self.iterazioni = 10000
        self.d = d

    def run(self):
        while(self.iterazioni > 0):
            sleep(0.1)
            self.iterazioni -= 1
            self.d.shift()
            
class Cuoco(Thread):
    
    piatti = [ "*", ";", "^", "%"]

    def __init__(self, d : RunningSushiBuffer):
        super().__init__()
        self.iterazioni = 1000
        self.d = d

    def run(self):
        while(self.iterazioni > 0):
            sleep(0.5 * random())
            self.iterazioni -= 1
            randPiatto = randint(0,len(self.piatti)-1)
            self.d.put(self.piatti[randPiatto])
            print ( f"Il cuoco {self.ident} ha cucinato <{self.piatti[randPiatto]}>")
        print ( f"Il cuoco {self.ident} ha finito il suo turno e va via")

class Cliente(Thread):
    
    def __init__(self, d : RunningSushiBuffer, pos : int):
        super().__init__()
        self.coseCheVoglioMangiare = randint(1,20)
        self.d = d
        self.pos = pos

    def run(self):
        while(self.coseCheVoglioMangiare > 0):
            sleep(5 * random())
            self.coseCheVoglioMangiare -= 1
            print ( f"Il cliente {self.ident} aspetta cibo")
            print ( f"Il cliente {self.ident} mangia <{self.d.get(self.pos)}>")
        print ( f"Il cliente {self.ident} ha la pancia piena e va via")


size = 20
D = RunningSushiBuffer(size)
NastroRotante(D).start()
for i in range(0,2):
    Cuoco(D).start()
for i in range(1,size):
    Cliente(D,i).start()