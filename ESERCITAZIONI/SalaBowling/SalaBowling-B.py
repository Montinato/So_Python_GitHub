from threading import Thread,Condition,Lock
from random import randint,random
from time import sleep


class Sala:
    
    def __init__(self,numeroPalle):
        print("SALA OK! ")
        self.piste = [ False , False]
        self.numeroPalle = numeroPalle
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.prossimo_da_servire = 1
        self.bollino = 1

    def richiediPista(self,numGiocatori):
        with self.lock:
            
            mioBollino = self.bollino
            self.bollino += 1
            while( mioBollino != self.prossimo_da_servire or numGiocatori > self.numeroPalle or self._cercaPista() == -1):
                print("La squadra con " + str(numGiocatori) + " giocatori deve attendere il suo turno con bollino " + str(mioBollino) )
                self.condition.wait()

            
            
            self.prossimo_da_servire += 1

            self.condition.notifyAll()

            self.numeroPalle -= numGiocatori

            p = self._cercaPista()
            

            self.piste[p] = True
            
            print(f"La squadra ottiene la pista {p} con {numGiocatori} giocatori e bollino {mioBollino}")
            return p

    def liberaPista(self,numPista,numGiocatori):
        with self.lock:
           
            print("La squadra finisce la partita e libera la pista.")
                
            self.numeroPalle += numGiocatori

            self.piste[numPista] = False

            self.condition.notifyAll()


    def _cercaPista(self):
        for i in range(0,len(self.piste)):
            if not self.piste[i]:
                return i 
        return -1


class Squadra(Thread):

    def __init__(self,sala,numGiocatori):
        super().__init__()
        self.sala = sala
        self.numGiocatori = numGiocatori

    def run(self):
        print("La squadra %s prova a richiedere la pista. "  % Squadra.getName(self))
        sleep(int((random()*6)))
        print("Sta giocando la squadra %s " % Squadra.getName(self))
        pista = self.sala.richiediPista(self.numGiocatori)

        print("I giocatori giocano sulla pista numero " + str(pista))


        sleep(5)
        
        
        self.sala.liberaPista(pista,self.numGiocatori)
        #print("La squadra %s lascia la pista  %d"   % Squadra.getName(self),str(pista) )
    


def main():

    print("START")

    sala = Sala(10)

    for i in range(0,10):
        x = randint(0,10)
        squadra = Squadra(sala,x)
        squadra.start()


if __name__ == "__main__":
    main()


