from threading import Lock,Condition
from Bacchetta import Bacchetta

class Tavolo:

    def __init__(self):
        self.__bacchetta = [ Bacchetta() for _ in range(5)]
        self.lock = Lock()
        self.cond = Condition(self.lock)

    def prendiLockSimultaneo(self,posizione):
        with self.lock:
            while( self.__bacchetta[posizione].checkOccupata() or self.__bacchetta[(posizione + 1) % 5].checkOccupata()):
                self.cond.wait()
                self.__bacchetta[posizione].prendi__bacchetta()
                self.__bacchetta[(posizione + 1) % 5].prendi__bacchetta()

    def mollaLockSimultaneo(self,posizione):
        with self.lock:
            self.__bacchetta[posizione].lascia_bacchetta()
            self.__bacchetta[(posizione + 1) % 5].lascia_bacchetta()
            self.cond.notifyAll()