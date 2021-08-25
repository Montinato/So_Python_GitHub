from threading import Thread,Condition,Lock
from random import randint,random
from time import sleep


class Campo:
    
    def __init__(self,numeroPalle):
        self.numeroPalle = numeroPalle
        self.lock = Lock()
        self.condition = Condition(self.lock)


    def noleggiaPalline(self,numPalle):
        with self.lock:
            while(self.numeroPalle < numPalle):
                self.condition.wait()
            
            print("Il giocatore ha bisogno di " + str(numPalle) + " per poter giocare e GIOCA!")
            self.numeroPalle -= numPalle


    def restituiscePalline(self,numPalle):
        with self.lock:
            while(self.numeroPalle == 0):
                self.condition.notifyAll()

            print("Il giocatore finisce la partita!")
            self.numeroPalle += numPalle
            



class Giocatore(Thread):
    
    def __init__(self,campo,numPalle):
        super().__init__()
        self.numPalle = numPalle
        self.campo = campo

    def run(self):
        while True:
            print("Il giocatore %s prova a noleggiare le palline" % Giocatore.getName(self))
            self.campo.noleggiaPalline(self.numPalle)
            sleep(2)
            self.campo.restituiscePalline(self.numPalle)
            print("Il giocatore %s restituisce le palline" % Giocatore.getName(self))



def main():
    random = randint(1,10)
    campo = Campo(random)

    random1 = randint(1,10)
    giocatore = Giocatore(campo,random1)

    giocatore.start()


if __name__ == '__main__':
    main()



