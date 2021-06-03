from Scrittore import Scrittore
from Lettore import Lettore
from DatoCondiviso import DatoCondiviso


dc = DatoCondiviso(999)

NUMS = 5
NUML = 5 

scrittori = [ Scrittore(i,dc) for i in range(NUMS)]

lettori = [ Lettore(i,dc) for i in range(NUML)]

for s in scrittori:
    s.start()

for l in lettori:
    l.start()