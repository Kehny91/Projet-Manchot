from Espace import Vecteur
from DataManagement import MDD

"""
L'ensemble des informations de vol
"""
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

    def setPosAvion(self, posAvion):
        self._posAvion = posAvion

    def setVAvion(self,vAvion):
        self._vAvion = vAvion

    def setAssiette(self, assiette):
        self._assiette = assiette


"""
L'ensemble des informations de vol protégés par MDD
"""
class MDDFlightData:
    def __init__(self, posAvion, vAvion, assiette):
        self._mdd = MDD(FlightData(posAvion,vAvion,assiette))

    def getPosAvion(self):
        return self._mdd.doOnData(FlightData.getPosAvion)

    def getVAvion(self):
        return self._mdd.doOnData(FlightData.getVAvion)

    def getAssiette(self):
        return self._mdd.doOnData(FlightData.getAssiette)

    def setPosAvion(self, posAvion):
        self._mdd.doOnData(FlightData.setPosAvion,posAvion)

    def setVAvion(self,vAvion):
        self._mdd.doOnData(FlightData.setVAvion,vAvion)

    def setAssiette(self, assiette):
        self._mdd.doOnData(FlightData.setAssiette,assiette)

    def get(self):
        return self._mdd.read()

    
   