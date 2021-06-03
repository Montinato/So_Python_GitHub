from threading import Lock

class Bacchetta:
    
    def __init__(self):
        #self.lock = Lock()         CAMBIAMO LA LOGICA DI ACCESSO ALLE BACCHETTE
        # PRIMA PRENDEVAMO UNA _bacchetta ALLA VOLTA, ADESSO ABBIAMO UN LOCK IN TAVOLO CON CUI PRENDIAMO SIMULTANEAMENTE DUE BACCHETTE
        # SE OVVIAMENTE NON SONO OCCUPATE
        self.occupata = False

    def checkOccupata(self):
        return self.occupata

    def prendi_bacchetta(self):
        #self.lock.acquire()
        self.occupata = True

    def lascia_bacchetta(self):
        #self.lock.release()
        self.occupata = False