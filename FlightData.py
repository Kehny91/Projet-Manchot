from Espace import Vecteur

class FlightData:
    def __init__(self, posAvion, vAvion, assiette):
        self._posAvion = posAvion
        self._vAvion = vAvion
        self._assiette = assiette

    def getPosAvion(self):
        return self._posAvion

    def getVAvion(self):
        return self._vAvion

    def getAssiette(self):
        return self._assiette

    def setPosAcion(self, posAvion):
        self._posAvion = posAvion

    def setVAvion(self,vAvion):
        self._vAvion = vAvion

    def setAssiette(self, assiette):
        self._assiette = assiette

    
   