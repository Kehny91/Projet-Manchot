from DataManagement import normalize

class FlightData:
    def __init__(self, x = 0, z = 0, v = 0, vz = 0, theta = 0):
        self._x = x
        self._z = z
        self._v = v
        self._vz = vz
        self._theta = theta
    
    def setX(self, x):
        self._x = x
    
    def getX(self):
        return self._x

    def setZ(self, z):
        self._z = z

    def getZ(self):
        return self._z

    def setV(self, v):
        self._v = v

    def getV(self):
        return self._v

    def setVz(self, vz):
        self._vz = vz

    def getVz(self):
        return self._vz

    def setTheta(self, theta):
        self._theta = normalize(theta)

    def getTheta(self):
        return normalize(self._theta)