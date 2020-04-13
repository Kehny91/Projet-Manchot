from math import sqrt
from DataManagement import constrain
from DataTypes import PilotInput,AutoPilotInput

class Asservissement:
    def __init__(self, mddPilotInput, mddFlightData, mddAutoPilotInput):
        self._mddPilotInput = mddPilotInput
        self._mddFlightData = mddFlightData
        self._mddAutoPilotInput = mddAutoPilotInput

        self._PThrottle = 0.1
        self._Passiette = 0.5

    def compute(self):
        consigne = self._mddAutoPilotInput.read()
        consigneVx = consigne.getVx()
        consigneVz = consigne.getVz()
        consigneV  = sqrt(consigneVx**2 + consigneVz**2)


        current = self._mddFlightData.read()
        currentVx = current.getVAvion().getX()
        currentVz = current.getVAvion().getZ()
        currentV  = sqrt(currentVx**2 + currentVz**2)

        throttle = constrain((consigneV-currentV)*self._PThrottle , 0, 1)
        pitch = constrain((consigneVz - currentVz)*self._Passiette,-1,1)
        flaps = 0

        self._mddPilotInput.write(PilotInput(pitch,flaps,throttle))


