from DataManagement import checkBoundaries
import time

class SystemeMeca:
    def __init__(self, value0, valueMin, valueMax):
        self._valueMin = valueMin
        self._valueMax = valueMax
        checkBoundaries(value0, valueMin, valueMax)
        self._value = value0
        self._lastT = time.time()
        self._consigne = value0

    def setConsigne(self, consigne):
        """Donne la consigne a atteindre"""
        checkBoundaries(consigne, self._valueMin, self._valueMax)
        self._consigne = consigne

    def getConsigne(self):
        return self._consigne

class Systeme1Ordre(SystemeMeca):
    def __init__(self, value0, valueMin, valueMax, tempsDeReaction):
        super(Systeme1Ordre,self).__init__(value0,valueMin,valueMax)
        self._tau = tempsDeReaction/3
    
    def _update(self, dt):
        self._value = (self._consigne/self._tau + self._value/dt)/(1.0/self._tau + 1.0/dt)
    
    def getValue(self):
        """Renvoie la valeur réelle"""
        t = time.time()
        self._update(max(0.000001, t - self._lastT))
        self._lastT = t
        return self._value

if __name__ == "__main__":
    from math import cos
    system = Systeme1Ordre(0,-10,10,0.2)
    t = 0
    for i in range(500):
        if (t>2):
            system.setConsigne(cos(t))
        print("consigne ",system.getConsigne())
        print("value ",system.getValue())
        print("")
        time.sleep(0.01)
        t += 0.01

def getThrustConsigne(percent, maxWatt, maxStaticThrust, v):
    # Un moteur a hélice développe une puissance P=V*T constante, pas une poussée constante.
    # Cependant si v==0 et notre moteur developpe 505W, on a T = P / V = 505 / 0
    # Cette regle ne s'applique pas aux basses vitesse car il faudrait prendre en compte la vitesse de l'air mise en mouvement par l'hélice
    # Ainsi, au basses vitesses, on considérera une poussée constante, au hautes vitesse, une puissance constante
    if (v<0.0001):
        return percent*maxStaticThrust
    else:
        return min(percent*maxStaticThrust,percent*maxWatt/v)
