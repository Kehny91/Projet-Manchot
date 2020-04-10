import threading as th
import time
from math import pi
from copy import copy

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

#Une boite au lettre avec ecrasement
class BAL_AE:
    def __init__(self, taille):
        self._taille = taille
        self._currentSize = 0
        self._placePrises = th.Semaphore(0)
        self._protection = th.Semaphore(1)
        self._data = []
    
    def pushValue(self,x):
        with self._protection:
            if self._taille == self._currentSize :
                self._data[-1] = x
            else:
                self._data.append(x)
                self._currentSize += 1
                self._placePrises.release()

    def pullValue(self):
        self._placePrises.acquire()
        with self._protection:
            out = self._data.pop(0)
            self._currentSize -= 1
        return out

#Un tableau noir (acces protégé)
class MDD:
    def __init__(self,value0):
        self._data = value0
        self._protection = th.Semaphore(1)
    
    def write(self,x):
        with self._protection:
            self._data = x

    def read(self):
        out = None
        with self._protection:
            out = copy(self._data)
        return out

    def doOnData(self,func,*args):
        out = None
        with self._protection:
            out = copy(func(self._data,*args))
        return out



#TESTS
if __name__=="__main__":

    class testouille:
        def __init__(self):
            self.u = 0
        
        def add(self,x):
            self.u += x
            print("on m'a rajouté ",x)

    mdd = MDD(testouille())

    

    def parleurFct():
        print("parleur Start")
        for i in range (20):
            toPush = i
            mdd.doOnData(testouille.add,2)
            print("je poste "+ str(toPush))
            time.sleep(0.1)

    def ecouteurFct():
        print("ecouteur Start")
        for i in range(20):
            res = mdd.read()
            print("J'ai lu " + str(res))
            time.sleep(0.8)

    parleur = th.Thread(target= parleurFct) #Parle lentement
    ecouteur = th.Thread(target = ecouteurFct) #Lit vite

    ecouteur.start()
    parleur.start()

    parleur.join()
    print("parleur a fini")
    ecouteur.join()
    print("ecouter a fini")
    print("All done")

    

