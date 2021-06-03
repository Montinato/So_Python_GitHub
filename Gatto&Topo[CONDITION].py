import random, time
from threading import Thread, Lock, Condition
from sys import version


class Striscia:

    LUNG = 20

    def __init__(self):
        self.lock = Lock()
        self.striscia = list()
        self.fine = False 
        self.dirGatto = 1
        self.topo = random.randint(0,self.LUNG-1)
        self.gatto = random.randint(0,self.LUNG-1)
        self.lock = Lock()

        self.posGatto = self.gatto
        self.posTopo = self.topo

        for i in range(0,self.LUNG):
            self.striscia.append(' ')
        self.striscia[self.topo] = 'T'
        self.striscia[self.gatto] = 'G'

        self.drawDisplay = Condition(self.lock)

    def printStriscia(self):
        with self.lock:
                if self.posGatto==self.gatto and self.posTopo == self.topo:
                    self.drawDisplay.wait()
                
                print("DISPLAY")
                print("|%s|" % ''.join(self.striscia))
                return self.fine    
        
    
    def muoviGatto(self):
        with self.lock:
                print("GATTO")
                if(self.fine):
                    return True
                
                self.striscia[self.gatto] = ' '

                self.gatto += self.dirGatto
                if(self.gatto > self.LUNG-1 or self.gatto<0):
                    self.dirGatto =- self.dirGatto 
                    self.gatto += 2*self.dirGatto

                if self.posGatto != self.gatto:
                    self.drawDisplay.notifyAll()
                    self.posGatto = self.gatto
                else:
                    print("La posizione del GATTO non cambia, quindi non stampo il DISPLAY")
                

                if(self.gatto == self.topo):
                    #self.drawDisplay.notifyAll()
                    self.fine = True 
                    self.striscia[self.gatto] = '@'
                    return True 
                
                
                self.striscia[self.gatto] = 'G'
                return False 
        
    def muoviTopo(self):
        with self.lock:
            print("TOPO")
            if(self.fine):
                return True

            self.striscia[self.topo] = ' '

            self.salto = random.randint(-1,1)
            if(self.topo + self.salto >= 0 and self.topo + self.salto < self.LUNG):
                self.topo = self.topo + self.salto

            if self.posTopo != self.topo:
                self.drawDisplay.notifyAll()
                self.posTopo = self.topo
            else:
                print("La posizione del TOPO non cambia, quindi non stampo il DISPLAY")

            if(self.gatto == self.topo):
                #self.drawDisplay.notifyAll()
                self.fine = True 
                self.striscia[self.topo] = '@'
                return True 
           
            

            self.striscia[self.topo] = 'T'
            return False 

class Gatto(Thread):

    def __init__(self,s):
        super().__init__()
        self.striscia = s

    def run(self):
        print("Gatto Start!")
        while(not striscia.muoviGatto()):
            time.sleep(0.100)


class Topo(Thread):

    def __init__(self,s):
        super().__init__()
        self.striscia = s

    def run(self):
        print("Topo Start!")
        while(not striscia.muoviTopo()):
            time.sleep(0.050)

class Display(Thread):
    
    def __init__(self,s):
        super().__init__()
        self.striscia = s

    def run(self):
        print("Display Start!")
        while(not striscia.printStriscia()):
            time.sleep(0.020)
        print("Il topo è stato NGAGGHIATO!")

# MAIN

print ("Start Gatto & Topo versione basic")
print ("Python version %s" % version)

striscia = Striscia()

jerry = Topo(striscia)

tom = Gatto(striscia)

display = Display(striscia)

print ("Creazione CHECK")

display.start()
jerry.start()
tom.start()

print ("RUN")