from threading import Thread,Lock,Condition
from queue import Queue
from random import Random

class ContoBancario:
    def __init__(self,s,id):
        self.id = id
        self.saldo = s
        self.listaMovimenti = [ Transazione ]
        self.lock = Lock()          # Perche??????

    def deposita(self,x):
        self.saldo += x
    
    def getId(self):
        return self.id

    def getListaMovimenti(self):
        return self.listaMovimenti

    def getLock(self):          # Perche??????
        return self.lock

    def getSaldo(self):
        return self.saldo

    def preleva(self,x):
        if self.saldo >= x:
            self.saldo-=x
            return True
        return False

    def setTransazione(self,s,d,v):
        transazione = Transazione(s,d,v)
        self.listaMovimenti.append(transazione)

        if(len(self.listaMovimenti)>50):
            self.listaMovimenti.pop(0)


class Transazione:

    def __init__(self,s,d,v):
        self.sorgente = s
        self.destinatario = d 
        self.value = v 

    def show(self):
        print("Sorgente: " + self.sorgente + " Destinatario " + self.destinatario + " Valore: " + self.value)

    def getDestinazione(self):
        return self.destinatario
    
    def getSorgente(self):
        return self.sorgente

    def getValue(self):
        return self.value



class Banca:

    def __init__(self):
        self.conti = { }
        
    
    def aggiungiConto(self,cc):
        if(self.conti.get(cc.getId())):
            raise NameError 
        else:
            self.conti.update(cc.getId(),cc)

    def getContiID(self):
        return self.conti.keys()


    def getSaldo(self,idConto):
        with self.lock_Saldo:
            contoBancario = self.conti.get(idConto)
            
            lock = contoBancario.getLock()
            
            with self.lock:
                return contoBancario.getSaldo()


    def trasferisci(self,idS,idD,V):
        sorgente = self.conti.get(idS)
        destinatario = self.conti.get(idD)

        lock_S = sorgente.getLock()
        lock_D = destinatario.getLock()

        if(idS < idD):
            lock_S.acquire()
            lock_D.acquire()
        else:
            lock_D.acquire()
            lock_S.acquire()

        if(sorgente.preleva(V)):
            destinatario.deposita(V)
            sorgente.setTransazione(idS,idD,V)
            destinatario.setTransazione(idS,idD,V)
            return True
        return False

        lock_S.release()
        lock_D.release()

        
class Cliente(Thread):

    def __init__(self,banca,contoB):
        super().__init__()
        self.banca = banca
        self.contoB = contoB 

    def run(self):
        mioContoID = self.contoB.getId()        # Mi prendo l'Id del ContoB
        destinatario = mioContoID

        while(destinatario):
            pass


        # NON COMPLETA
    
