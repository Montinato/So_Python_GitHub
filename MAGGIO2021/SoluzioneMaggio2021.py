#!/usr/bin/python3

from threading import RLock, Condition, Thread
from time import sleep
from random import random

class Sala:
    
    def __init__(self, num_piste, num_palle):
        
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.num_piste = num_piste
        self.pista = [False] * num_piste
        self.palleDisponibili = num_palle
        
        # self.prossimo_da_servire = 1
        # self.bollino = 1
        self.prossimoID = 1
        self.listaAttesa = []

    #
    # Versione precedente fornita ai candidati a superare l'esame
    #
    def OLD_richiediPista(self, id_squadra, numGiocatori):
        
        with self.lock:
            mioBollino = self.bollino
            self.bollino += 1
            while (self.__cercaPista() == -1 or 
                   self.palleDisponibili < numGiocatori or 
                   mioBollino != self.prossimo_da_servire):
                
                    print(f"La squadra {id_squadra} con {numGiocatori} giocatori deve attendere il suo turno con bollino {mioBollino}")
                    self.condition.wait()
                
            #  fa scorrere il turno 
            self.prossimo_da_servire += 1
            #  si da la possibilita' immediata di provare a giocare al prossimo numero da servire 
            self.condition.notifyAll()
            self.palleDisponibili -= numGiocatori
            p = self.__cercaPista()
            self.pista[p] = True
            print(f"La squadra {id_squadra} ottiene la pista {p} con {numGiocatori} giocatori e bollino {mioBollino}")
            return p

    #
    #  Nuova versione modificata
    # 
    def richiediPista(self, id_squadra, numGiocatori, modalitaGentile = False):
        
        with self.lock:
            
            # VECCHIO MODO DI METTERSI IN CODA
            # mioBollino = self.bollino
            # self.bollino += 1
            
            # NUOVO MODO DI METTERSI IN CODA
            self.listaAttesa.append(id_squadra)         # Aggiungo la squadra in posizione 0 della nuova lista
            # 

            while (self.__cercaPista() == -1 or 
                   self.palleDisponibili < numGiocatori or 
                   id_squadra != self.listaAttesa[0]):
                    # NUOVO. E' GIA' IL MIO TURNO MA NON CI SONO RISORSE PER GIOCARE
                    if modalitaGentile and id_squadra == self.listaAttesa[0]:
                        self.listaAttesa.pop(0)
                        print(f"La squadra {id_squadra} con {numGiocatori} giocatori rimanda il suo turno")
                        if len(self.listaAttesa) >= 4:
                            self.listaAttesa.insert(3,id_squadra)
                        else:
                            self.listaAttesa.append(id_squadra)
                    #######
                    print(f"La squadra {id_squadra} con {numGiocatori} giocatori deve attendere il suo turno")
                    self.condition.wait()
                
            #  fa scorrere il turno 
            #  self.prossimo_da_servire += 1
            #  NUOVO MODO DI SCORRERE IL TURNO
            self.listaAttesa.pop(0)

            self.condition.notifyAll()
            self.palleDisponibili -= numGiocatori
            p = self.__cercaPista()
            self.pista[p] = True
            print(f"La squadra {id_squadra} ottiene la pista {p} con {numGiocatori} giocatori")
            return p

    #
    #  Metodo la cui implementazione era richiesta
    #
    def richiediPistaGentilmente(self, id_squadra, numGiocatori):
        
        return self.richiediPista(id_squadra,numGiocatori,True)



    def liberaPista(self, numPista, numGiocatori):
        with self.lock:
            self.palleDisponibili += numGiocatori
            self.pista[numPista] = False
            self.condition.notifyAll()

    def __cercaPista(self):
        for i in range(0,len(self.pista)):
            if not self.pista[i]:
                return i
        return -1



class Squadra(Thread):

    def __init__(self, id, sala):
        super(Squadra, self).__init__()
        self.sala = sala
        self.id = id

    def run(self):
        while True:
            
            #  il giocatore fa altro prima di chiedere una pista
            sleep(int((random() * 6)))
            #  prova a chiedere una pista
            numGiocatori = int((random() * 20))+1
            print(f"La squadra {self.id} chiede una pista per {numGiocatori} giocatori.")
            pista = self.sala.richiediPistaGentilmente(self.id, numGiocatori)
            print(f"La squadra {self.id} gioca sulla pista {pista} .")
            #  tempo di gioco
            sleep(int((random() * 4)))
            self.sala.liberaPista(pista, numGiocatori)
            print(f"La squadra {self.id} lascia la pista {pista}.")

if __name__ == '__main__':
    s = Sala(3, 20)
    for i in range(0,5):
        Squadra(i, s).start()