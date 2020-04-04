import DataManagement as dm

class AutoPilotInput:
    """ La classe représentant les entrées demandée par l'autopilote
        v : La vitesse absolue demandée, en m/s
        vz : Le taux de montee demandé, en m/s"""
    def __init__(self, v, vz):
        self._v = v
        self._vz = vz

    def getV(self):
        return self._v

    def setV(self, v):
        self._v = v

    def getVz(self):
        return self._vz

    def setVz(self, vz):
        self._vz = vz

class PilotInput:
    """ La classe représentant les entrées demandée par un pilote
        pitch : La commande de tanguage: positif = cabrer  [Entre -1 et 1]
        flaps : La commande des flaps: positif = sortis [Entre 0 et 1]
        throttle : La commande moteur  [Entre 0 et 1]"""
    def __init__(self,pitch,flaps,throttle):
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
        return self._flaps
    
    def setThrottle(self, throttle):
        dm.checkBoundaries(throttle, 0, 1)
        self._throttle = throttle



    

class RawInput:
    def __init__(self, elevG, elevD, flapsG, flapsD, throttle):
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