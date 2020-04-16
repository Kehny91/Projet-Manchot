import DataManagement as dm
from DataManagement import MDD
from math import sqrt

class AutoPilotInput:
    """ La classe représentant les entrées demandée par l'autopilote
        v : Le vecteur vitesse demandé"""
    def __init__(self, v):
        dm.checkBoundaries(v.getX(),0,None)
        self._v = v

    def getV(self):
        return self._v

    def setV(self, v):
        dm.checkBoundaries(v.getX(),0,None)
        self._v = v

    def setVx(self, vx):
        dm.checkBoundaries(vx,0,None)
        self._v.x = vx

    def getVx(self):
        return self._v.getX()

    def setVz(self,vz):
        self._v.z = vz

    def getVz(self):
        return self._v.getZ()
    
class PilotInput:
    """ La classe représentant les entrées demandée par un pilote
        pitch : La commande de tanguage: positif = cabrer  [Entre -1 et 1]
        flaps : La commande des flaps: positif = sortis [Entre 0 et 1]
        throttle : La commande moteur  [Entre 0 et 1]"""
    def __init__(self, pitch = 0, flaps = 0, throttle = 0):
        dm.checkBoundaries(pitch,-1,1)
        self._pitch = pitch

        dm.checkBoundaries(flaps,0,1)
        self._flaps = flaps

        dm.checkBoundaries(throttle,0,1)
        self._throttle = throttle
    
    def getPitch(self):
        return self._pitch
    
    def setPitch(self, pitch):
        dm.checkBoundaries(pitch, -1, 1)
        self._pitch = pitch

    def getFlaps(self):
        return self._flaps
    
    def setFlaps(self, flaps):
        dm.checkBoundaries(flaps, 0, 1)
        self._flaps = flaps

    def getThrottle(self):
        return self._throttle
    
    def setThrottle(self, throttle):
        dm.checkBoundaries(throttle, 0, 1)
        self._throttle = throttle
    

class RawInput:
    def __init__(self, elevG = 0, elevD = 0, flapsG = 0, flapsD = 0, throttle = 0):
        """La classe représentatn les entrée brutes des différent actionneurs
        elevG : La commande de la gouverne arriere gauche (VTAIL) [Entre -1 et 1]
        elevD : La commande de la gouverne arriere droite [Entre -1 et 1]
        flapsG : La commande du volet gauche [Entre 0 et 1]
        flapsD : La commande du volet droit [Entre 0 et 1]
        throttle : La commande du throttle [Entre 0 et 1]"""
        dm.checkBoundaries(elevG, -1, 1)
        self._elevG = elevG

        dm.checkBoundaries(elevD, -1, 1)
        self._elevD = elevD

        dm.checkBoundaries(flapsG, 0, 1)
        self._flapsG = flapsG

        dm.checkBoundaries(flapsD, 0, 1)
        self._flapsD = flapsD

        dm.checkBoundaries(throttle, 0, 1)
        self._throttle = throttle

    def getElevG(self):
        return self._elevG

    def setElevG(self, elevG):
        dm.checkBoundaries(elevG, -1, 1)
        self._elevG = elevG

    def getElevD(self):
        return self._elevD

    def setElevD(self, elevD):
        dm.checkBoundaries(elevD, -1, 1)
        self._elevD = elevD

    def getFlapsG(self):
        return self._flapsG

    def setFlapsG(self, flapsG):
        dm.checkBoundaries(flapsG, 0, 1)
        self._flapsG = flapsG

    def getFlapsD(self):
        return self._flapsD

    def setFlapsD(self, flapsD):
        dm.checkBoundaries(flapsD, 0, 1)
        self._flapsD = flapsD

    def getThrottle(self):
        return self._throttle

    def setThrottle(self, throttle):
        dm.checkBoundaries(throttle, 0, 1)
        self._throttle = throttle

    #Renvoie un dictionnaire, pret a etre propagé dans le modele
    def getInputDict(self):
        return {"elevG" : self._elevG,
                "elevD" : self._elevD,
                "flapsG" : self._flapsG,
                "flapsD" : self._flapsD,
                "throttle" : self._throttle}


class RapportDeCollision:
    def __init__(self, pos1 = None, force1 = None, pos2 = None, force2 = None):
        self.pos1 = pos1
        self.force1 = force1
        self.pos2 = pos2
        self.force2 = force2
    
    def addImpact(self, pos, force):
        if (self.pos1 == None and self.force1==None):
            self.pos1 = pos
            self.force1 = force
        elif (self.pos2 == None and self.force2 == None):
            self.pos2 = pos
            self.force2 = force
        else:
            assert False, "Trop d'impactes"

    def getPos1(self):
        return self.pos1

    def getPos2(self):
        return self.pos2

    def getForce1(self):
        return self.force1

    def getForce2(self):
        return self.force2

"""
L'ensemble des informations de vol
"""
class FlightData:
    def __init__(self, posAvion, vAvion, assiette, w):
        self._posAvion = posAvion
        self._vAvion = vAvion
        self._assiette = assiette
        self._w = w
        self._time = 0

    def getPosAvion(self):
        return self._posAvion

    def getVAvion(self):
        return self._vAvion

    def getAssiette(self):
        return self._assiette

    def setPosAvion(self, posAvion):
        self._posAvion = posAvion

    def setVAvion(self,vAvion):
        self._vAvion = vAvion

    def setAssiette(self, assiette):
        self._assiette = assiette

    def setW(self, w):
        self._w = w

    def getW(self):
        return self._w

    def setTime(self, t):
        self._time = t

    def getTime(self):
        return self._time