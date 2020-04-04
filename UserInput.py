class AutoPilotInput:
    """ La classe représentant les entrées demandée par l'autopilote
        v : La vitesse absolue demandée, en m/s
        vz : Le taux de montee demandé, en m/s"""
    def __init__(self, v, vz):
        self.v = v
        self.vz = vz

class PilotInput:
    """ La classe représentant les entrées demandée par un pilote
        pitch : La commande de tanguage: positif = cabrer  [Entre -1 et 1]
        flaps : La commande des flaps: positif = sortis [Entre 0 et 1]
        throttle : La commande moteur  [Entre 0 et 1]"""
    def __init__(self,pitch,flaps,throttle):
        self.pitch = pitch
        self.flaps = flaps
        self.throttle = throttle

class RawInput:
    def __init__(self, elevG, elevD, flapsG, flapsD, throttle):
        """La classe représentatn les entrée brutes des différent actionneurs
        elevG : La commande de la gouverne arriere gauche (VTAIL) [Entre -1 et 1]
        elevD : La commande de la gouverne arriere droite [Entre -1 et 1]
        flapsG : La commande du volet gauche [Entre 0 et 1]
        flapsD : La commande du volet droit [Entre 0 et 1]
        throttle : La commande du throttle [Entre 0 et 1]"""
        self.elevG = elevG
        self.elevD = elevD
        self.flapsG = flapsG
        self.flapsD = flapsD
        self.throttle = throttle