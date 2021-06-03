from threading import Lock,Condition,Thread
from queue import Queue
from time import sleep
from random import random,randint

# CLASSE BARBIERE OK 

class Barbiere(Thread):

    def __init__(self,negozio):
        super().__init__()
        self.negozio=negozio

    def run(self):
        while True:
            self.negozio.nextCliente()

# CLASSE CLIENTE OK 

class Cliente(Thread):

    def __init__(self,negozio):
        super().__init__()
        self.negozio = negozio 
        self.zazzera =randint(2000,50000)

    def run(self):
        self.negozio.entra(self)

# CLASSE NEGOZIO OK, HO MODIFICATO ENTRA E NEXTCLIENTE

class Negozio:
    def __init__(self,numeroPosti):
        self.numeroPosti = numeroPosti
        self.sedie = Queue(self.numeroPosti)
        self.lock_attesa = Lock()
        self.lock_taglio = Lock()
        self.conditionAttesa = Condition(self.lock_attesa)
        self.conditionTaglio = Condition(self.lock_taglio)
        #self.clienteAlTaglio = -1
        self.pieni = False
        self.poltrona = -1


    def entra(self,cliente):

        # Il cliente entra nel negozio e prova a sedersi per aspettare 
        if self.sedie.full():
            return 

        # Se invece ci sono posti liberi, entra e viene aggiunto alla Queue
        self.sedie.put(cliente)

        # Una volta aggiunto, controllo che il Cliente sia diverso dal barbiere 
        # Con self.poltrona = -1 identifico il barbiere che quando non ha clienti dorme sulla poltrona 
        with self.lock_attesa:
            print("ENTRA "+"Cliente=" + cliente.getName() + " self.poltrona=" + self.poltrona + "\n")

            while(cliente.getName() == self.poltrona):
                self.conditionAttesa.wait()

        # Il cliente aspetta il proprio turno
        with self.lock_taglio:
            print("ENTRA "+"Il Cliente %s aspetta il proprio turno " % (cliente.getName()))
            while(cliente.zazzera > 0):
                self.conditionTaglio.wait()


    def nextCliente(self):

        with self.lock_attesa:
            self.poltrona = -1
            cliente = self.sedie.get()

        #with self.lock_attesa:
            self.poltrona = cliente.getName()
            print("NEXTCLIENTE "+"Il Cliente %s e' seduto sulla poltrona " % (cliente.getName()))
            self.conditionAttesa.notifyAll()
        
        print("NEXTCLIENTE "+"Cliente al taglio %s . \n" % (cliente.getName()))

        with self.lock_taglio:
            while(cliente.zazzera > 0):
                cliente.zazzera-=1

            print("NEXTCLIENTE "+"Il Cliente %s ha finito " % (cliente.getName()))
            
            self.conditionTaglio.notifyAll()




# MAIN 


def main():
    negozio = Negozio (11)
    barbiere = Barbiere(negozio)

    #   clienti = [ Cliente(negozio) for i in range (0,11)]

    #   for c in clienti:
    #    c.start()

    barbiere.start()


    while True:
        cliente = Cliente(negozio).start()
        #sleep(2)


if __name__=='__main__':
    main()



   