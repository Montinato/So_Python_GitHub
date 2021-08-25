from threading import Thread,Condition,Lock
from random import randint,Random
from queue import Queue
from time import sleep

class Negozio:
    def __init__(self,numeroPosti):
        self.sedie = Queue(numeroPosti)
        self.lockAttesa = Lock()
        self.lockTaglio = Lock()
        self.conditionAttesa = Condition(self.lockAttesa)
        self.conditionTaglio = Condition(self.lockTaglio)
        #self.condition = Condition(self.lock)

    def entra(self,cliente):

        if self.sedie.full():
            return 

        self.sedie.put(cliente)

        
        with self.lockTaglio:    
            while(cliente.zazzera > 0):
                self.conditionTaglio.wait()
           

    def prossimoCliente(self):
        #print("ENTRO IN PROSSIMO CLIENTE")
        with self.lockAttesa:
            while(not self.sedie.empty):
                self.conditionAttesa.notifyAll()
                sleep(5)
                cliente = self.sedie.get()
        with self.lockTaglio:
            print("bbbbbbbbbbbbb")
            
            while(cliente.zazzera > 0):
                cliente.zazzera -= 1

            self.conditionTaglio.notifyAll()
            print("aaaaaaaaaaaaaaaaaaa")

            print("Il barbiere finisce di servire il cliente " + cliente + "\n")
                    
class Barbiere(Thread):
    def __init__(self,negozio):
        super().__init__()
        self.negozio = negozio

    def run(self):
        while(True):
            sleep(5)
            print("Il barbiere %s e' pronto a servire un nuovo cliente." % Barbiere.getName(self))
            self.negozio.prossimoCliente()
            

class Cliente(Thread):

    nextId = 0

    def __init__(self,negozio):
        super().__init__()
        self.negozio = negozio
        self.zazzera = randint(10,1000)

    def run(self):
        print("Il Cliente %s entra nel negozio" % Cliente.getName(self))
        self.negozio.entra(self)


def main():
    
    print("START!")

    negozio = Negozio(10)
    barbiere = Barbiere(negozio)


    barbiere.start()

    clienti = [ Cliente(negozio) for i in range(0,10)]
    for c in clienti:
        c.start()




if __name__ == "__main__":
    main()


# NON FUNZIONA