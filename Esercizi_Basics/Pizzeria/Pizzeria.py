from threading import Thread,Condition,Lock
from queue import Queue
from time import sleep
from random import random,randint
from enum import Enum


class Ordine:

    def __init__(self,cod,q):
        self.cod = cod
        self.q = q 

class Pizzeria:
    
    def __init__(self):
        self.bufferOrdini = Queue(20)
        self.bufferPizze = list(10)
        self.lock = Lock()
        self.conditionOrdini = Condition(self.lock)
        self.conditionPizze = Condition(self.lock)
        self.bufferOrdiniPieno = False
        self.bufferPizzePieno = False


    def putOrdine(self,cliente):           # Il cliente effettua l'ordine
        with self.lock:

            print("Il Cliente %s entra nel negozio ed effettua l'ordine  "  %cliente.getName())
            while( self.bufferOrdini.full() ):
                self.conditionOrdini.wait()

                cP = randint(1,4)
                q = randint(1,10)
                ordine = Ordine(cP,q)
                self.conditionPizze.notifyAll()
                return ordine

            

    
    def getOrdine(self):        # Il Pizzaiolo preleva l'ordine 
        with self.lock:
            while( len(self.bufferPizze) == 0):
                self.conditionPizze.wait() 

                value = self.bufferOrdini.get()
                self.bufferPizze.append(value)    

                print("Il pizzaiolo preleva l'ordine ... ")

                self.conditionOrdini.notifyAll()      

                return value
            

    def putPizze(self):        # Il Pizzaiolo prende l'ordine e fa le pizze 
        with self.lock:
            while ( not len(self.bufferPizze) == 0 ):
                self.conditionOrdini.wait()

                self.bufferPizze.append(self.bufferOrdini.get())

                self.conditionPizze.notifyAll()




    def getPizze(self):         # Il Cliente appena sono pronte le pizze le preleva
        with self.lock:
            while( len(self.bufferPizze) == 0 ):
                self.conditionPizze.wait()

                self.bufferPizze.pop()

                self.conditionOrdini.notifyAll()



class Pizzaiolo(Thread):
    
    def __init__(self,pizzeria):
        super().__init__()
        self.pizzeria = pizzeria 

    def run(self):
        while True:
            print("Il pizzaiolo " + self.getName() + " controlla se ci sono ordini ...")

            ordine = self.pizzeria.getOrdine()     # Prende un ordine

            tempoDiPreparazione = ordine.quantita

            print("Il pizzaiolo " + self.getName() + "ha prelevato l'ordine numero " + str(ordine.codiceOrdine))

            sleep(tempoDiPreparazione*1)
            ordine.prepara()

            print("Il pizzaiolo " + self.getName() + " ha preparato le pizze per l'ordine numero " + str(ordine.codiceOrdine))

            self.pizzeria.putPizze(ordine)

            # Bomba...

            sleep(randint(1,25))



class TipoPizza(Enum):
    Margherita = 1
    QuattroStagioni = 2 
    Capricciosa = 3


class Cliente(Thread):

    def __init__(self,pizzeria):
        super().__init__()
        self.pizzeria = pizzeria 

    
    def run(self):
        while True:
            numeroPizze = 1 + randint(0,7)
            codicePizza = TipoPizza(randint(1,3))

            print("Il Cliente " + self.getName() + " entra in pizzeria e prova ad ordinare delle pizze ")

            ordine = self.pizzeria.putOrdine(codicePizza,numeroPizze)

            print("IL Cliente " + self.getName() + " aspetta le pizze con codice d'ordine numero " + str(ordine.codiceOrdine))

            sleep(randint(0,numeroPizze*1))         # ASPETTA UN POCO 
            self.pizzeria.getPizze(ordine)          # PRENDE L'ORDINE

            print("Il Cliente " + self.getName() + " ha preso le pizze con codice d'ordine numero " + str(ordine.codiceOrdine))
            print(ordine.pizze)


            sleep(randint(0,numeroPizze*1))


class Ordine:
    nextCodiceOrdine = 0

    def __init__(self,tipoPizza,quantita):
        self.tipoPizza = tipoPizza
        self.quantita = quantita
        self.codiceOrdine = Ordine.nextCodiceOrdine
        self.pizze = ""
        Ordine.nextCodiceOrdine += 1

    def prepara(self):
        for i in range(0,self.quantita):
            self.pizze += "(*)"

# #   Dalla traccia noto che le operazioni bloccanti riguardano il BufferPizze 
# #   Quindi creao un BlockingSet che mi permette di gestire queste operazioni

# class BlockingSet(set):
#     lock = Lock()
#     condition = Condition(lock)
#     tagliaMassima = 10

#     def add(self,_T):
#         with self.lock:
#             while len(self) == self.tagliaMassima:
#                 self.condition.wait()

#             self.condition.notifyAll()
#             return super().add(_T)

#     def remove(self,_T):
#         with self.lock:
#             retValue = _T in self
#             while not retValue:
#                 self.condition.wait()
#                 retValue = _T in self 

#             super().remove(_T)
#             self.condition.notifyAll()
#             return retValue




# class Pizzeria:
#     blockingQueue = Queue(10)
#     blockingSet = BlockingSet()


#     def getOrdine(self):
#         try:
#             return self.blockingQueue.get()
#         finally:
#             pass
#         return None

#     def getPizze(self,ordine):
#         self.blockingSet.remove(ordine)

#     def putOrdine(self,codicePizza,quantita):
#         ordine = Ordine(codicePizza,quantita)
#         try:
#             self.blockingQueue.put(ordine)
#         finally:
#             pass
#         return ordine

#     def putPizze(self,ordine):
#         self.blockingSet.add(ordine)


def main():
    p = [Pizzaiolo] * 3
    c = [Cliente] * 10
    pizzeria = Pizzeria()

    for i in range(0, 3):
        p[i] = Pizzaiolo(pizzeria)
        p[i].start()

    for i in range(0, 10):
        c[i] = Cliente( pizzeria)
        c[i].start()

if __name__ == '__main__':
    main()