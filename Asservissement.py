from math import sqrt
from DataManagement import constrain
class Asservissement:
    def __init__(self, mddPilotInput, mddFlightData, mddAutoPilotInput):
        self._mddPilotInput = mddPilotInput
        self._mddFlightData = mddFlightData
        self._mddAutoPilotInput = mddAutoPilotInput

        self._PThrottle = 0.1
        self._Passiette = 0.5

    def compute(self):
        consigneVx = self._mddAutoPilotInput.getVx()
        consigneVz = self._mddAutoPilotInput.getVz()
        consigneV  = sqrt(consigneVx**2 + consigneVz**2)
        
        currentVx = self._mddFlightData.getVAvion().getX()
        currentVz = self._mddFlightData.getVAvion().getZ()
        currentV  = sqrt(currentVx**2 + currentVz**2)

        throttle = constrain((consigneV-currentV)*self._PThrottle , 0, 1)
        pitch = constrain((consigneVz - currentVz)*self._Passiette,-1,1)

        self._mddPilotInput.setPitch(pitch)
        self._mddPilotInput.setThrottle(throttle)


