import DataManagement as dm

class AutoPilotInput:
    """ La classe représentant les entrées demandée par l'autopilote
        v : Le vecteur vitesse demandé"""
    def __init__(self, v):
        self._v = v

    def getV(self):
        return self._v

    def setV(self, v):
        self._v = v


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
    def getInputVector(self):
        return {"elevG" : self._elevG,
                "elevD" : self._elevD,
                "flapsG" : self._flapsG,
                "flapsD" : self._flapsD,
                "throttle" : self._throttle}





#TESTS
if __name__ == "__main__":
    rawInput = RawInput(0,0,0,0,0)
    rawInput.setElevD(-1)
    rawInput.setElevG(-0.8)
    rawInput.setFlapsD(0.1)
    rawInput.setFlapsG(0.3)
    rawInput.setThrottle(0.5)
    print(str(rawInput.__dict__))
    try:
        rawInput.setFlapsD(-0.1)
    except dm.OutOfBoundException:
        print("Unauthorized")
    print(rawInput.getInputVector())

    pilotInput = PilotInput(0,0,0)
    pilotInput.setFlaps(0.1)
    pilotInput.setPitch(0.2)
    pilotInput.setThrottle(0.3)
    print(str(pilotInput.__dict__))
    try:
        pilotInput.setThrottle(1.1)
    except:
        print("Unauthorized")

    autoPilotInput = AutoPilotInput(0,0)
    autoPilotInput.setV(0.1)
    autoPilotInput.setVz(-0.1)
    print(str(autoPilotInput.__dict__))