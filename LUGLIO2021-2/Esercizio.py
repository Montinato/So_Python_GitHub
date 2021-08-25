from threading import RLock, Thread,Condition
from queue import Queue,Empty
from random import random,randint
from time import sleep

class Frame:
    def __init__(self,s,d,m):
        self.MAC_Sorgente = s
        self.MAC_Destinazione = d
        self.messaggio = m
        #
        # Porta di provenienza. Valorizzata da un worker al momento del prelievo
        #
        self.__provenienza = None


class Porta:
    def __init__(self):
        self.N = 20
        # Buffer di ingresso
        self.in_ = Queue(self.N)
        # Buffer di uscita
        self.out = Queue(self.N)


class Switch:

    def __init__(self,NPorte,NWorker):
        self.switchTable = {}
        self.lock = RLock()
        self.porte = [Porta() for i in range(0,NPorte)]
        self.workers = [Worker(self) for i in range(0,NWorker)] 

        # LO SWITCH ALL'AVVIO CREERA' TANTI WORKER E LI FARA' INIZIARE A GIRARE 
        for i in range(0,NWorker):
            ########  ATTENZIONE #########
            # LA RUN DEL WORKER LAVORA ATTRAVERSO I METODI PRIVATI __GETFRAME() e __PUTFRAME()
            self.workers[i].start()

        # Aggiungo un array di Conditions
        self.conditions = [Condition() for i in range(0,NPorte)]

    def __aggiornaChiave(self, s, p):
        with self.lock:
            self.switchTable[s] = p

    def __leggiChiave(self, s):
        with self.lock:
            print(self.switchTable.get(s))
            print("\n")
            return self.switchTable.get(s)

    def sendFrame(self,f : Frame, p : Porta):
        print("Inserisco il Frame: \n")
        print("MAC_SORGENTE : %s \n" % f.MAC_Sorgente)
        print("MAC_DESTINAZIONE : %s \n" % f.MAC_Destinazione)
        print("MESSAGGIO : %s \n" % f.messaggio)
        print("Nella porta con indice %s" % p)
        p.in_.put(f)

    def receiveFrame(self,p : Porta):
        print("Prelevo il Frame dalla porta di indice %s \n" % p)
        #return self.porte[p].out.get()
        return p.out.get()
        

    def __putFrame(self, f : Frame):
        with self.lock: 
            port = self.__leggiChiave(f.MAC_Destinazione)
            
            if port != None:
                print("Stampo port= %s \n" % port)
                port.out.put(f)
                print("Inserisco il Frame: \n")
                print("MAC_SORGENTE : %s \n" % f.MAC_Sorgente)
                print("MAC_DESTINAZIONE : %s \n" % f.MAC_Destinazione)
                print("MESSAGGIO : %s \n" % f.messaggio)
                # print("UNICAST %s : %s->%s = %s" % (port,f.MAC_Sorgente,f.MAC_Destinazione,f.messaggio))
            else:
                print("BROADCAST")
                for i in range(0,len(self.porte)):
                    if self.porte[i] != f.__provenienza:
                        self.porte[i].out.put(f)
                        print("%s : %s->%s" % (self.porte[i],f.MAC_Sorgente,f.MAC_Destinazione))
                        #self.conditions[i].notifyAll()


    def __getFrame(self):
        with self.lock:
            for i in range(0,len(self.porte)):
                try :
                    f = self.porte[i].in_.get_nowait()
                    if f != None:
                        f.__provenienza = self.porte[i]
                        #while(self.porte[i].in_.qsize() == 0):
                        #    self.conditions[i].wait()
                        self.__aggiornaChiave(f.MAC_Sorgente, f.__provenienza)
                        return f
                except Empty:
                    pass
            return None


class Worker(Thread):

    def __init__(self, s : Switch):
        super(Worker, self).__init__()
        self.s = s

    def run(self):
        while True:
            sleep(2)
            print("\n")
            print("WORKER \n")
            f = self.s._Switch__getFrame()
            if f != None:
                self.s._Switch__putFrame(f)



destinations = [ "01:01:01:01:01:01", 
                 "01:01:01:01:01:02", 
                 "01:01:01:01:01:03", 
                 "01:01:01:01:01:04",
                 "01:01:01:01:01:05"]

class FrameGenerator(Thread):

    def __init__(self,s : Switch, porta : Porta, mac : str):
        super(FrameGenerator, self).__init__()
        self.porta = porta 
        self.mac = mac
        self.s = s

    def run(self):
        while(True):
            sleep(0)
            print("\n")
            print("FRAME GENERATOR \n")
            sleep(random())
            # IL FRAME GENERATOR INVECE LAVORA ATTRAVERSO IL METODO SENDFRAME(). COSTRUTTORE FRAME -> def __init__(self,s,d,m):
            self.s.sendFrame(Frame(self.mac,destinations[randint(0,4)],"Lorem Ipsum:"+chr(randint(64,84))),self.porta)
            sleep(0.5)
            self.s.receiveFrame(self.porta)


if __name__ == '__main__':

    # CREO UNO SWITCH e RUNNO I WORKER CON I METODI PRIVATI _PUTFRAME() e _GETFRAME()
    cisco2900 = Switch(5,2)
    
    # CREO UN FRAME GENERATOR e RUNNO ATTRAVERSO IL METODO SENDFRAME() 
    generators = [FrameGenerator(cisco2900,cisco2900.porte[i],"01:01:01:01:01:0"+chr(ord("1")+i)) for i in range(0,5)]
    for gen in generators:
        gen.start()

