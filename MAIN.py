
from math import cos,sin,pi
import time
import threading as th
import Mixer
import PyQt5
from Espace import Vecteur,Referentiel,ReferentielAbsolu
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal,QObject
from Asservissement import Asservissement
from DataManagement import MDD,Pauser
import Parametres
import Modes as M
import Espace as E
import Drone as D
from Solide import refSol

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

class Physique:
    def __init__(self, world, flightData):
        # definition du modele
        self.drone = D.Drone(world)
        self.drone.setVitesseBati(flightData.getVAvion())
        self.drone.setAssiette(E.normalise(flightData.getAssiette()))
        self.drone.setPositionBati(flightData.getPosAvion())

    def mettreAJourModeleAvecRawInput(self, rawInputDict):
        # Propagation du dictionnaire d'input dans le modele.
        self.drone.diffuseDictRawInput(rawInputDict)

    def compute(self, flightData, dt):
        # modele mis a jour
        # Compute sera appele en boucle par le PhysicThread
        self.drone.structure.update(dt)
        # Retourne un nouveau flight data
        flightData.setPosAvion(self.drone.getPositionBati())
        flightData.setAssiette(E.normalise(self.drone.getAssiette()))
        flightData.setVAvion(self.drone.getVitesseBati())
        flightData.setW(self.drone.getVitesseRot())
        flightData.setTime(flightData.getTime()+dt)
        return flightData

class PhysicThread(th.Thread):
    def __init__(self,world, mddFlightData, mddRawInput, frequence, dilatation):
        super(PhysicThread,self).__init__()
        self._mddFlightData = mddFlightData
        self._mddRawInput = mddRawInput
        self._period = 1/frequence
        self._continue = True
        self._physique = Physique(world, self._mddFlightData.read())
        self._world = world
        self._dilatation = dilatation

    def run(self):
        while self._continue:
            tStartTour = time.time()
            current = self._mddFlightData.read()
            rawInput = self._mddRawInput.read()
            self._world.update(self._period/self._dilatation)
            self._physique.mettreAJourModeleAvecRawInput(rawInput.getInputDict())
            newFlightData = self._physique.compute(current, self._period/self._dilatation)
            self._mddFlightData.write(newFlightData)
            Logger.pushNewLine(newFlightData, rawInput, self._physique.drone.generateRapportCollision())
            waiting = self._period - (time.time() - tStartTour)
            if (waiting<0):
                print("Surcharge CPU, retard de ", -1*waiting)
            else:
                time.sleep(waiting)
    
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
        self._lastMode = -1
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
    from Parametres import ParametresSimulation as PS
    from IHM.ihm import IHM
    from DataTypes import RawInput,PilotInput,AutoPilotInput,FlightData,RapportDeCollision,World,VentGlobal,VentLocal,Obstacle,Sol
    from DataManagement import MDD
    import sys
    import PyQt5.Qt as Qt
    from Logger import Logger

    Logger.setup(str(int(time.time())))

    referentielSol = refSol

    mddFlightData = MDD(FlightData(Vecteur(PS.positionXIni,PS.positionZIni,referentielSol),Vecteur(PS.vitesseXIni,PS.vitesseZIni,referentielSol), PS.assietteIni, PS.wIni), True)
    mddRawInput = MDD(RawInput(0.0,0.0,0.0,0.0,0.0), False)
    mddPilotInput = MDD(PilotInput(0,0,0), False)
    mddAutoPilotInput = MDD(AutoPilotInput(Vecteur(0,0,referentielSol)), True)
    mddMode = MDD(M.MODE_PILOT)
    
    

    world = World(PS.scaleAffichage, PS.positionXPiste,PS.longueurXPiste,referentielSol)
    world.addObstacle(Sol(referentielSol))
    world.addObstacle(Obstacle(Vecteur(30,0,referentielSol),Vecteur(100,5,referentielSol), referentielSol))
    world.addPerturbation(VentGlobal(Vecteur(PS.VentMoyenVitesseX,PS.VentMoyenVitesseZ,referentielSol),PS.VentVariationAmplitude,PS.VentRapiditeVarition,referentielSol,))
    #world.addPerturbation(VentLocal(Vecteur(0,5,referentielSol),0,5,referentielSol,Vecteur(15,0,referentielSol),10))

    mT = MixerThread(mddRawInput,mddPilotInput,PS.frequenceMixer)
    mT.start()

    mddMode.write(PS.modeInitial)

    if not PS.logOnly:
        app = Qt.QApplication(sys.argv)
        mainW = Qt.QMainWindow()
        graph = IHM(world, mddFlightData, mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput, PS.frequenceAffichage)
        graph.startUpdateThread()
        graph.artificiallyPressButton(PS.modeInitial)
        mainW.setCentralWidget(graph)
        mainW.show()

    

    pT = PhysicThread(world, mddFlightData,mddRawInput, PS.frequencePhysique, PS.dilatation)
    pT.start()

    aT = AsserThread(mddFlightData,mddAutoPilotInput,mddPilotInput,PS.frequenceAsservissement)
    aT.start()
    aT.requestPause()

    sT = ScriptThread(mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput)
    sT.start()
    sT.requestPause()

    mmT = ModeManagerThread(mddMode,mT,aT,sT)
    mmT.start()

    if not PS.logOnly:
        app.exec_()
        graph.stopUpdateThread()
    else:
        input("Appuiez sur entree pour arreter la simulation\n")
    
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