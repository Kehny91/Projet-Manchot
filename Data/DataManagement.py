import threading as th
import time
from math import pi
from copy import copy,deepcopy

class OutOfBoundException(Exception):
    pass

def checkBoundaries(x, xMin, xMax):
    if (xMin != None and x<xMin):
        raise OutOfBoundException()
    if (xMax != None and x>xMax):
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
    def __init__(self,value0,useDeepCopy = False):
        """Si la classe contenue a des objets complexes (Vecteur par exemple), il faut utiliser la deepcopy"""
        self._data = value0
        self._protection = th.Semaphore(1)
        self._useDeepCopy = useDeepCopy
    
    def write(self,x):
        with self._protection:
            if (self._useDeepCopy):
                self._data = deepcopy(x)
            else:
                self._data = copy(x)

    def read(self):
        out = None
        with self._protection:
            if (self._useDeepCopy):
                out = deepcopy(self._data)
            else:
                out = copy(self._data)
        return out

    def doOnData(self,func,*args):
        out = None
        with self._protection:
            if (self._useDeepCopy):
                out = deepcopy(func(self._data,*args))
            else:
                out = copy(func(self._data,*args))
        return out

class Pauser:
    def __init__(self):
        self._semaphore = th.Semaphore(0)
        self._pauseRequested = False
        self._someoneIsSleeping = False

    def requestPause(self):
        self._pauseRequested = True

    def unpause(self):
        self._pauseRequested = False
        if (self._someoneIsSleeping):
            self._semaphore.release()

    def check(self):
        if (self._pauseRequested):
            self._someoneIsSleeping = True
            self._semaphore.acquire()
            #Ok, on m'a libéré
            self._someoneIsSleeping = False


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

    

