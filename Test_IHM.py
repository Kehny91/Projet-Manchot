
from math import cos,sin
import time
import threading as th
import Mixer
import PyQt5
from PyQt5 import Qt

class Vecteur:
    def __init__(self,x,z):
        self.x = x
        self.z = z
    def getX(self):
        return self.x
    def getZ(self):
        return self.z
    def __add__(self,other):
        return Vecteur(self.x+other.x, self.z + other.z)
    def __sub__(self,other):
        return Vecteur(self.x-other.x, self.z - other.z)
    def __mul__(self,scal):
        return Vecteur(self.x*scal, self.z *scal)
    def rotate(self,angle):
        return Vecteur(self.x*cos(angle)-self.z*sin(angle),self.z*cos(angle)+self.x*sin(angle))
    def withZmin(self,zMin):
        return Vecteur(self.x,max(zMin,self.z))

class MixerThread(th.Thread):
    def __init__(self,mddRawInput,mddPilotInput):
        super().__init__()
        self.mddRawInput = mddRawInput
        self.mddPilotInput = mddPilotInput

    def run(self):
        while True:
            Mixer.Mixer.mix(self.mddPilotInput,self.mddRawInput)
            time.sleep(0.300)

class UpdateThread(Qt.QThread):
    def __init__(self,ihm):
        super().__init__()
        self.ihm = ihm
    
    def run(self):
        while True:
            self.ihm.refresh()
            time.sleep(0.1)



if __name__ == "__main__":
    from IHM.ihm import IHM
    from FlightData import MDDFlightData
    from UserInput import MDDRawInput, MDDPilotInput, MDDAutoPilotInput
    #from Espace import Vecteur
    import sys
    import PyQt5.Qt as Qt

    mddFlightData = MDDFlightData(Vecteur(0,1),Vecteur(1,-0.1),-0.3)
    mddRawInput = MDDRawInput(0.30,0.30,0.50,0.50,0.100) 
    mddPilotInput = MDDPilotInput(0,0,0)
    mddAutoPilotInput = MDDAutoPilotInput(Vecteur(0,0))
    
    mT = MixerThread(mddRawInput,mddPilotInput)
    mT.start()

    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = IHM(mddFlightData,mddRawInput,0,mddAutoPilotInput,mddPilotInput)
    uT = UpdateThread(graph)
    uT.start()
    mainW.setCentralWidget(graph)
    mainW.show()
    graph.update()
    sys.exit(app.exec_())