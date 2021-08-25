from threading import Thread,Lock,Condition
from time import sleep
from random import randint,random

class Ponte:
    
    def __init__(self,verso):
        self.verso = verso          # 0 -> da Mare a Montagna, 1 -> da Montagna a Mare
        self.lock = Lock()
        self.condition = Condition()
        self.numeroTuristi = 0
        self.sogliaGiri = 3
        self.contaGiri = 0


    def cambioVerso(self):

        with self.lock:
            while(True):
                if randint(1,5) > 3:
                    if(self.verso == 0):
                        self.verso = 1
                        print("\n")
                        print("IL VERSO DEL PONTE E' CAMBIATO")
                        print("\n")
                    else:
                        self.verso = 0
                        print("\n")
                        print("IL VERSO DEL PONTE NON CAMBIA QUESTA VOLTA")
                        print("\n")
                    
                        
                        
                    self.condition.notifyAll()
            return

    def arrivoSulPonte(self,turista):

        with self.lock:
            while(self.numeroTuristi == 0 and self.verso != turista.destinazione and self.numeroTuristi > 3 
                    and self.numeroTuristi > self.sogliaGiri):
                self.condition.wait()
            
            self.numeroTuristi += 1

            if self.verso != turista.destinazione:
                print("CAMBIA IL VERSO DI PERCORRENZA DEL PONTE")
                self.verso = turista.destinazione
                self.numeroTuristi = 1
            
            print("Il turista percorre il verso giusto ... ")



    def attraversoIlPonte(self,turista):

        with self.lock:
            while(self.verso == turista.destinazione and (self.numeroTuristi > 0 and self.numeroTuristi <= self.sogliaGiri) ):
                self.condition.notifyAll()
            
            self.numeroTuristi -= 1
            print("Il turista lascia il ponte.")
        

    

class Turista(Thread):
    
    def __init__(self,ponte,partenza,destinazione):
        super().__init__()
        self.ponte = ponte
        self.partenza = partenza
        self.destinazione = destinazione

    def run(self):
        print("Il Turista %s e' pronto ad attraversare il ponte" % Turista.getName(self))
        sleep(5)
        self.ponte.arrivoSulPonte(self)
        sleep(5)
        
        print("Il Turista %s sta attraversando il ponte" % Turista.getName(self))
        self.ponte.attraversoIlPonte(self)
        sleep(5)

        #self.ponte.cambioVerso()
        

def main():

    verso = randint(0,1)

    p = Ponte(verso)

    x = randint(1,10)

    t = [ Turista ] * x

    for i in range(0,x):

        var = randint(0,20)

        if(var > 10):
            par = 0
            dest = 1
        else:
            par = 1
            dest = 0

        t[i] = Turista(p,par,dest)
        t[i].start()


if __name__ == "__main__":
    main()




