from math import pi
TORAD = pi/180
TODEG = 180/pi
TOMpS = 1/3.6

class ParametresModele:
    flapsGMaxAngle      = 45*TORAD      #Radians
    flapsDMaxAngle      = 45*TORAD      #Radians
    elevDMaxAngle       = 20*TORAD      #Radians
    elevGMaxAngle       = 20*TORAD      #Radians
    engineMaxThrust     = 200           #Newton
    maxAutoPilotSpeed   = 200*TOMpS     #m/s
    maxAutoPilotZSpeed  = 20*TOMpS      #m/s