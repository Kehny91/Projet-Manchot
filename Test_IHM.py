
from math import cos,sin
import time
import threading as th
import Mixer
import PyQt5
from Espace import Vecteur,Referentiel,ReferentielAbsolu
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal,QObject
from Asservissement import Asservissement
from DataManagement import MDD,Pauser
import Modes as M

class MixerThread(th.Thread):
    def __init__(self,mddRawInput,mddPilotInput,frequence):
        super().__init__()
        self._mddRawInput = mddRawInput
        self._mddPilotInput = mddPilotInput
        self._period = 1.0/frequence
        self._continue = True
        self._pauser = Pauser()

    def run(self):
        while self._continue:
            self._pauser.check()
            Mixer.Mixer.mix(self._mddPilotInput,self._mddRawInput)
            time.sleep(self._period)

    def stop(self):
        self._continue = False

    def unpause(self):
        self._pauser.unpause()

    def requestPause(self):
        self._pauser.requestPause()

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


class AsserThread(th.Thread):
    def __init__(self, mddFlightData, mddAutoPilotInput, mddPilotInput, frequence):
        super(AsserThread,self).__init__()
        self._mddFlightData = mddFlightData
        self._mddAutoPilotInput = mddAutoPilotInput
        self._mddPilotInput = mddPilotInput
        self._period = 1/frequence
        self._continue = True
        self._asser = Asservissement(mddPilotInput,mddFlightData,mddAutoPilotInput)
        self._pauser = Pauser()

    def run(self):
        while self._continue:
            self._pauser.check()
            self._asser.compute()
            time.sleep(self._period)

    def stop(self):
        self._continue = False

    def unpause(self):
        self._pauser.unpause()

    def requestPause(self):
        self._pauser.requestPause()

class ModeManagerThread(th.Thread):
    def __init__(self,mddMode, mixerT, asserT): #TODO SCRIPT
        super(ModeManagerThread,self).__init__()
        self._mddMode = mddMode
        self._mixerT = mixerT
        self._asserT = asserT
        self._lastMode = mddMode.read()
        self._continue = True

    def run(self):
        while self._continue:
            mode = self._mddMode.read()
            if (mode != self._lastMode):
                self._lastMode = mode
                if mode == M.MODE_PILOT:
                    self._mixerT.unpause()
                    self._asserT.requestPause()
                elif mode == M.MODE_AUTO_PILOT:
                    self._mixerT.unpause()
                    self._asserT.unpause()
                elif mode == M.MODE_SCRIPT_RAW:
                    self._mixerT.requestPause()
                    self._asserT.requestPause()

    def stop(self):
        self._continue = False
        self._mixerT.unpause()
        self._asserT.unpause()



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
    mddMode = MDD(M.MODE_PILOT)
    
    mT = MixerThread(mddRawInput,mddPilotInput,100)
    mT.start()
    

    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = IHM(mddFlightData, mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput, 60)
    graph.startUpdateThread()
    mainW.setCentralWidget(graph)
    mainW.show()

    cT = CinematiqueThread(mddFlightData,50)
    cT.start()

    aT = AsserThread(mddFlightData,mddAutoPilotInput,mddPilotInput,200)
    aT.start()
    aT.requestPause()

    mmT = ModeManagerThread(mddMode,mT,aT)
    mmT.start()

    app.exec_()
    graph.stopUpdateThread()
    mmT.stop()
    mT.stop()
    cT.stop()
    aT.stop()