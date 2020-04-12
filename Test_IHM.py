
from math import cos,sin
import time
import threading as th
import Mixer
import PyQt5
from Espace import Vecteur,Referentiel,ReferentielAbsolu
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal,QObject

class MixerThread(th.Thread):
    def __init__(self,mddRawInput,mddPilotInput,frequence):
        super().__init__()
        self._mddRawInput = mddRawInput
        self._mddPilotInput = mddPilotInput
        self._period = 1.0/frequence
        self._continue = True

    def run(self):
        while self._continue:
            Mixer.Mixer.mix(self._mddPilotInput,self._mddRawInput)
            time.sleep(self._period)

    def stop(self):
        self._continue = False

class CinematiqueThread(th.Thread):
    def __init__(self,mddFlightData,frequence):
        super(CinematiqueThread,self).__init__()
        self._mddFlightData = mddFlightData
        self._period = 1/frequence
        self._continue = True

    def run(self):
        while self._continue:
            v = self._mddFlightData.getVAvion()
            pos = self._mddFlightData.getPosAvion()
            pos = pos + v*self._period
            self._mddFlightData.setPosAvion(pos)
            time.sleep(self._period)
    
    def stop(self):
        self._continue = False

if __name__ == "__main__":
    from IHM.ihm import IHM
    from FlightData import MDDFlightData
    from UserInput import MDDRawInput, MDDPilotInput, MDDAutoPilotInput
    #from Espace import Vecteur
    import sys
    import PyQt5.Qt as Qt

    referentielSol = Referentiel("referentielSol",0,Vecteur(0,0))

    mddFlightData = MDDFlightData(Vecteur(0,1,referentielSol),Vecteur(1,-0.1,referentielSol),0.3)
    mddRawInput = MDDRawInput(0.30,0.30,0.50,0.50,0.100) 
    mddPilotInput = MDDPilotInput(0,0,0)
    mddAutoPilotInput = MDDAutoPilotInput(Vecteur(0,0,referentielSol))
    
    mT = MixerThread(mddRawInput,mddPilotInput,100)
    mT.start()
    

    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = IHM(mddFlightData, 0, mddRawInput, mddPilotInput, mddAutoPilotInput, 60)
    graph.startUpdateThread()
    mainW.setCentralWidget(graph)
    mainW.show()

    cT = CinematiqueThread(mddFlightData,50)
    cT.start()

    app.exec_()
    graph.stopUpdateThread()
    mT.stop()
    cT.stop()