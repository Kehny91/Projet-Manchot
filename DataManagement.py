import threading as th
import time
from math import pi


class OutOfBoundException(Exception):
    pass

def checkBoundaries(x, xMin, xMax):
    if (x<xMin or x>xMax):
        raise OutOfBoundException()

def constrain(x, xMin, xMax):
    return min(xMax,max(xMin,x))

def moduloF(x, modulo):
    if x>=0:
        return x - (x//modulo)*modulo
    else:
        return x - (x//modulo+1)*modulo

def normalize(angle):
    """ Permet de renvoyer un angle quelconque dans l'intervalle ]-pi , pi]"""
    angle = moduloF(angle, 2*pi)

    if -pi<angle and angle<=pi:
        return angle
    elif angle<=-pi:
        return normalize(angle + 2*pi)
    elif angle>pi:
        return normalize(angle - 2*pi)


#Une boite au lettre sans ecrasement
class BAL_SE:
    def __init__(self, taille):
        self._placesLibres = th.Semaphore(taille)
        self._placesPrises = th.Semaphore(0)
        self._protection = th.Semaphore(1)
        self._data = []

    def pushValue(self, x):
        self._placesLibres.acquire()
        with self._protection:
            self._data.append(x)
            self._placesPrises.release()

    def pullValue(self):
        self._placesPrises.acquire()
        with self._protection:
            out = self._data.pop(0)
            self._placesLibres.release()
        return out

#Une boite au lettre taille 1 avec ecrasement
class MDD:
    def __init__(self):
        self._placePrises = th.Semaphore(0)
        self._protection = th.Semaphore(1)
        self._data = 0
        self._empty = True 
    
    def pushValue(self,x):
        with self._protection:
            self._data = x
            if self._empty:
                self._placePrises.release()
            self._empty = False

    def pullValue(self):
        self._placePrises.acquire()
        with self._protection:
            out = self._data
            self._empty = True
        return out





#TESTS
if __name__=="__main__":
    mdd = BAL_SE(10)

    def parleurFct():
        for i in range (20):
            toPush = input()
            mdd.pushValue(toPush)
            print("je poste "+ str(toPush))
            time.sleep(0.01)

    def ecouteurFct():
        for i in range(20):
            res = mdd.pullValue()
            print("J'ai lu " + str(res))
            time.sleep(3)

    parleur = th.Thread(target= parleurFct) #Parle lentement
    ecouteur = th.Thread(target = ecouteurFct) #Lit vite

    ecouteur.start()
    parleur.start()

    parleur.join()
    print("parleur a fini")
    ecouteur.join()
    print("ecouter a fini")
    print("All done")

    

