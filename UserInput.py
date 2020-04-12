import DataManagement as dm
from DataManagement import MDD
from math import sqrt

class AutoPilotInput:
    """ La classe représentant les entrées demandée par l'autopilote
        v : Le vecteur vitesse demandé"""
    def __init__(self, v):
        self._v = v

    def getV(self):
        return self._v

    def setV(self, v):
        self._v = v

    def setVx(self, vx):
        self._v.x = vx

    def setVz(self,vz):
        self._v.z = vz

class MDDAutoPilotInput:
    """ La classe représentant les entrées demandée par l'autopilote protege par MDD
        v : Le vecteur vitesse demandé"""
    def __init__(self, v):
        self._mdd = MDD(AutoPilotInput(v))

    def getV(self):
        return self._mdd.doOnData(AutoPilotInput.getV)

    def setV(self, v):
        self._mdd.doOnData(AutoPilotInput.setV,v)

    def setVx(self, vx):
        self._mdd.doOnData(AutoPilotInput.setVx,vx)

    def setVz(self,vz):
        self._mdd.doOnData(AutoPilotInput.setVz,vz)

    
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

class MDDPilotInput:
    """ La classe représentant les entrées demandée par un pilote protegee par un MDD
        pitch : La commande de tanguage: positif = cabrer  [Entre -1 et 1]
        flaps : La commande des flaps: positif = sortis [Entre 0 et 1]
        throttle : La commande moteur  [Entre 0 et 1]"""
    def __init__(self, pitch = 0, flaps = 0, throttle = 0):
        self._mdd = MDD(PilotInput(pitch,flaps,throttle))
    
    def getPitch(self):
        return self._mdd.doOnData(PilotInput.getPitch)
    
    def setPitch(self, pitch):
        self._mdd.doOnData(PilotInput.setPitch,pitch)

    def getFlaps(self):
        return self._mdd.doOnData(PilotInput.getFlaps)
    
    def setFlaps(self, flaps):
        self._mdd.doOnData(PilotInput.setFlaps,flaps)

    def getThrottle(self):
        return self._mdd.doOnData(PilotInput.getThrottle)
    
    def setThrottle(self, throttle):
        self._mdd.doOnData(PilotInput.setThrottle,throttle)

    

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
    def getInputVector(self):
        return {"elevG" : self._elevG,
                "elevD" : self._elevD,
                "flapsG" : self._flapsG,
                "flapsD" : self._flapsD,
                "throttle" : self._throttle}


class MDDRawInput:
    def __init__(self, elevG = 0, elevD = 0, flapsG = 0, flapsD = 0, throttle = 0):
        """La classe représentatn les entrée brutes des différent actionneurs protegee par un MDD
        elevG : La commande de la gouverne arriere gauche (VTAIL) [Entre -1 et 1]
        elevD : La commande de la gouverne arriere droite [Entre -1 et 1]
        flapsG : La commande du volet gauche [Entre 0 et 1]
        flapsD : La commande du volet droit [Entre 0 et 1]
        throttle : La commande du throttle [Entre 0 et 1]"""
        self._mdd = MDD(RawInput(elevG, elevD, flapsG, flapsD, throttle))

    def getElevG(self):
        return self._mdd.doOnData(RawInput.getElevG)

    def setElevG(self, elevG):
        self._mdd.doOnData(RawInput.setElevG,elevG)

    def getElevD(self):
        return self._mdd.doOnData(RawInput.getElevD)

    def setElevD(self, elevD):
        self._mdd.doOnData(RawInput.setElevD, elevD)

    def getFlapsG(self):
        return self._mdd.doOnData(RawInput.getFlapsG)

    def setFlapsG(self, flapsG):
        self._mdd.doOnData(RawInput.setFlapsG,flapsG)

    def getFlapsD(self):
        return self._mdd.doOnData(RawInput.getFlapsD)

    def setFlapsD(self, flapsD):
        self._mdd.doOnData(RawInput.setFlapsD,flapsD)

    def getThrottle(self):
        return self._mdd.doOnData(RawInput.getThrottle)

    def setThrottle(self, throttle):
        self._mdd.doOnData(RawInput.setThrottle,throttle)

    #Renvoie un dictionnaire, pret a etre propagé dans le modele
    def getInputVector(self):
        return self._mdd.doOnData(RawInput.getInputVector)