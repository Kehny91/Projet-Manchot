
from math import cos,sin,pi
import time
import threading as th
import Mixer
import PyQt5
from AlexPhy.Espace import Vecteur,Referentiel,ReferentielAbsolu
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal,QObject
from Asservissement import Asservissement
from DataManagement import MDD,Pauser
import Parametres
import Modes as M
import AlexPhy.Solide as S
import AlexPhy.Espace as E

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

class LaPhysiqueDeTom:
    def __init__(self, flightData, referentielSol):
        # definition du modele
        self.planeur = S.Planeur(referentielSol)
        self.planeur.setAssiette(E.normalise(flightData.getAssiette()))
        self.planeur.setPositionBati(flightData.getPosAvion())
        self.planeur.setWCG(flightData.getW())
        self.planeur.setVitesseBati(flightData.getVAvion())

    def mettreAJourModeleAvecRawInput(self, rawInputDict):
        # Propagation du dictionnaire d'input dans le modele.
        # planeur.structure.setPosAvion
        self.planeur.diffuseDictRawInput(rawInputDict)
        # Mise a jour des Cz, alpha etc...
        # Ne retourne rien

    def compute(self, flightData, dt):
        # Grace au modele fraichement mis a jour, cette methode renvoie le nouveau flight data
        # Compute sera appelé en boucle par le PhysicThread
      
        self.planeur.setAssiette(E.normalise(flightData.getAssiette()))
        self.planeur.setPositionBati(flightData.getPosAvion())
        self.planeur.setWCG(flightData.getW())
        self.planeur.setVitesseBati(flightData.getVAvion())

        self.planeur.structure.update(dt)

        flightData.setPosAvion(self.planeur.getPositionBati())
        flightData.setAssiette(E.normalise(self.planeur.getAssiette()))
        flightData.setVAvion(self.planeur.getVitesseBati())
        flightData.setW(self.planeur.getVitesseRot())
        flightData.setTime(flightData.getTime()+dt)
        # Retourne un nouveau flight data
        return flightData
        

class PhysiqueDunObjetUniquementSoumisASonInertie(LaPhysiqueDeTom):
    def __init__(self):
        super(PhysiqueDunObjetUniquementSoumisASonInertie,self).__init__()

    def compute(self, flightData, dt):
        pos = flightData.getPosAvion()
        v = flightData.getVAvion()
        flightData.setPosAvion(pos+v*dt)
        return flightData


DILATATION = 5
class PhysicThread(th.Thread):
    def __init__(self,mddFlightData, mddRawInput, referentielSol, frequence):
        super(PhysicThread,self).__init__()
        self._mddFlightData = mddFlightData
        self._mddRawInput = mddRawInput
        self._period = 1/frequence
        self._continue = True
        self._physique = LaPhysiqueDeTom(self._mddFlightData.read(), referentielSol)

    def run(self):
        while self._continue:
            current = self._mddFlightData.read()
            rawInput = self._mddRawInput.read()
            self._physique.mettreAJourModeleAvecRawInput(rawInput.getInputDict())
            newFlightData = self._physique.compute(current, self._period/DILATATION)
            self._mddFlightData.write(newFlightData)
            Logger.pushNewLine(newFlightData, rawInput, RapportDeCollision())
            time.sleep(self._period)
    
    def stop(self):
        self._continue = False


class ScriptThread(th.Thread):
    def __init__(self,mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput):
        super(ScriptThread,self).__init__()
        self._script = Parametres.ParametresSimulation.scriptToLoad(mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput)
        self._continue = True
        self._pauser = Pauser()
    
    def run(self):
        if (self._script != None):
            while self._continue:
                self._script.runScript()
                self._pauser.check()

    def stop(self):
        self.unpause()
        if (self._script != None):
            self._script.stop()
        self._continue = False

    def unpause(self):
        self._script.reset()
        self._pauser.unpause()

    def requestPause(self):
        self._pauser.requestPause()
        if (self._script != None):
            self._script.stop()


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
        self.unpause()
        self._continue = False

    def unpause(self):
        self._pauser.unpause()

    def requestPause(self):
        self._pauser.requestPause()

class ModeManagerThread(th.Thread):
    def __init__(self,mddMode, mixerT, asserT, scriptT):
        super(ModeManagerThread,self).__init__()
        self._mddMode = mddMode
        self._mixerT = mixerT
        self._asserT = asserT
        self._scriptT = scriptT
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
                    self._scriptT.requestPause()
                elif mode == M.MODE_AUTO_PILOT:
                    self._mixerT.unpause()
                    self._asserT.unpause()
                    self._scriptT.requestPause()
                elif mode == M.MODE_SCRIPT_RAW:
                    self._mixerT.requestPause()
                    self._asserT.requestPause()
                    self._scriptT.unpause()
                elif mode == M.MODE_SCRIPT_PILOT:
                    self._mixerT.unpause()
                    self._asserT.requestPause()
                    self._scriptT.unpause()
                elif mode == M.MODE_SCRIPT_AUTOPILOT:
                    self._mixerT.unpause()
                    self._asserT.unpause()
                    self._scriptT.unpause()
            time.sleep(0.2)

    def stop(self):
        self._continue = False
        self._mixerT.unpause()
        self._asserT.unpause()



if __name__ == "__main__":
    from IHM.ihm import IHM
    from DataTypes import RawInput,PilotInput,AutoPilotInput,FlightData,RapportDeCollision
    from DataManagement import MDD
    import sys
    import PyQt5.Qt as Qt
    from Logger import Logger

    Logger.setup(str(int(time.time())))

    referentielSol = Referentiel("referentielSol",0,Vecteur(0,0))

    mddFlightData = MDD(FlightData(Vecteur(0,10,referentielSol),Vecteur(40,0,referentielSol), 0.1, 0), True)
    mddRawInput = MDD(RawInput(0.30,0.30,0.50,0.50,0.100), False)
    mddPilotInput = MDD(PilotInput(0,0,0), False)
    mddAutoPilotInput = MDD(AutoPilotInput(Vecteur(0,0,referentielSol)), True)
    mddMode = MDD(M.MODE_PILOT)
    
    mT = MixerThread(mddRawInput,mddPilotInput,100)
    mT.start()
    

    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = IHM(mddFlightData, mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput, 60)
    graph.startUpdateThread()
    mainW.setCentralWidget(graph)
    mainW.show()

    pT = PhysicThread(mddFlightData,mddRawInput, referentielSol, 100)
    pT.start()

    aT = AsserThread(mddFlightData,mddAutoPilotInput,mddPilotInput,150)
    aT.start()
    aT.requestPause()

    sT = ScriptThread(mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput)
    sT.start()
    sT.requestPause()

    mmT = ModeManagerThread(mddMode,mT,aT,sT)
    mmT.start()

    app.exec_()
    graph.stopUpdateThread()
    mmT.stop()
    mT.stop()
    pT.stop()
    aT.stop()
    sT.stop()
    Logger.stop()

    mmT.join()
    #print("Mode Manager Off")

    mT.join()
    #print("Mixer Off")

    pT.join()
    #print("Physic Off")

    aT.join()
    #print("Asser Off")

    sT.join()
    #print("Script Off")