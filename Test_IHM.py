
from math import cos,sin
import time
import threading as th
import Mixer
import PyQt5
from Espace import Vecteur,Referentiel,ReferentielAbsolu
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal,QObject

class MixerThread(th.Thread):
    def __init__(self,mddRawInput,mddPilotInput):
        super().__init__()
        self.mddRawInput = mddRawInput
        self.mddPilotInput = mddPilotInput

    def run(self):
        while True:
            Mixer.Mixer.mix(self.mddPilotInput,self.mddRawInput)
            time.sleep(0.01)

class UpdateThread(Qt.QThread,QObject):
    refreshPlease = pyqtSignal()

    def __init__(self,mddFlightData,referentielSol):
        super(UpdateThread,self).__init__()
        self.mddFlightData = mddFlightData
        self.referentielSol = referentielSol
    
    def run(self):
        while True:
            mddFlightData.setPosAvion(mddFlightData.getPosAvion()+Vecteur(0.001,0,self.referentielSol))
            self.refreshPlease.emit()
            time.sleep(0.005)



if __name__ == "__main__":
    from IHM.ihm import IHM
    from FlightData import MDDFlightData
    from UserInput import MDDRawInput, MDDPilotInput, MDDAutoPilotInput
    #from Espace import Vecteur
    import sys
    import PyQt5.Qt as Qt

    referentielSol = Referentiel("referentielSol",0,Vecteur(0,0))


    mddFlightData = MDDFlightData(Vecteur(0,0,referentielSol),Vecteur(0,-0.1,referentielSol),0.3)
    mddRawInput = MDDRawInput(0.30,0.30,0.50,0.50,0.100) 
    mddPilotInput = MDDPilotInput(0,0,0)
    mddAutoPilotInput = MDDAutoPilotInput(Vecteur(0,0,referentielSol))
    
    mT = MixerThread(mddRawInput,mddPilotInput)
    mT.start()

    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = IHM(mddFlightData,mddRawInput,0,mddAutoPilotInput,mddPilotInput)
    uT = UpdateThread(mddFlightData,referentielSol)
    uT.refreshPlease.connect(graph.refresh)
    uT.start()
    mainW.setCentralWidget(graph)
    mainW.show()
    graph.update()
    sys.exit(app.exec_())