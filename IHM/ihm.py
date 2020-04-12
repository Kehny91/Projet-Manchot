from IHM.Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from IHM.Widgets.EngineWidget import EngineWidget
from IHM.Widgets.GraphWidget import GraphWidget
from IHM.Widgets.SliderControlWidget import SliderControlWidget
import PyQt5.QtWidgets as QtWidgets
import PyQt5
from Test_IHM import Vecteur
from Parametres import ParametresModele
from PyQt5.QtCore import pyqtSignal,QObject
from PyQt5 import Qt
from math import pi
import time
TORAD = pi/180.0
TODEG = 180.0/pi

class _UpdateThread(Qt.QThread,QObject):
    refreshPlease = pyqtSignal()

    def __init__(self,mddFlightData,frequenceAffichage):
        super(_UpdateThread,self).__init__()
        self._mddFlightData = mddFlightData
        self._period = 1.0/frequenceAffichage
        self._continue = True
    
    def run(self):
        while self._continue:
            self.refreshPlease.emit()
            time.sleep(self._period)

    def stop(self):
        self._continue = False

class _GraphicalRawInput(QtWidgets.QWidget):
    def __init__(self,mddRawInput):
        super(_GraphicalRawInput,self).__init__()
        self._myLayout = QtWidgets.QVBoxLayout(self)

        self._affFlapsG = ControlSurfaceWidget(self,ParametresModele.flapsGMaxAngle,"flapsG",mddRawInput.getFlapsG)
        self._myLayout.addWidget(self._affFlapsG)

        self._affFlapsD = ControlSurfaceWidget(self,ParametresModele.flapsDMaxAngle,"flapsD",mddRawInput.getFlapsD)
        self._myLayout.addWidget(self._affFlapsD)

        self._affElevG = ControlSurfaceWidget(self,ParametresModele.elevGMaxAngle,"elevG",mddRawInput.getElevG)
        self._myLayout.addWidget(self._affElevG)

        self._affElevD = ControlSurfaceWidget(self,ParametresModele.elevDMaxAngle,"elevD",mddRawInput.getElevD)
        self._myLayout.addWidget(self._affElevD)

        self._affEngine = EngineWidget(self,ParametresModele.engineMaxThrust,"engine", mddRawInput.getThrottle)
        self._myLayout.addWidget(self._affEngine)

    def refresh(self):
        self._affElevD.refresh()
        self._affElevG.refresh()
        self._affEngine.refresh()
        self._affFlapsD.refresh()
        self._affFlapsG.refresh()


class IHM(QtWidgets.QWidget):
    def __init__(self, mddFlightData, mddRawInput, mddMode, mddAutoPilotInput, mddPilotInput, frequenceAffichage):
        super().__init__()
        self.mddFlightData = mddFlightData
        self.mddRawInput = mddRawInput
        self.mddMode = mddMode
        self.mddAutoPilotInput  = mddAutoPilotInput
        self.mddPilotInput = mddPilotInput


        self.myLayout = QtWidgets.QGridLayout(self)
        self.myLayout.setColumnMinimumWidth(0,50)
        self.myLayout.setColumnStretch(0,2)
        self.myLayout.setColumnMinimumWidth(1,50)
        self.myLayout.setColumnStretch(1,2)
        self.myLayout.setColumnMinimumWidth(2,50)
        self.myLayout.setColumnStretch(2,2)
        self.myLayout.setColumnMinimumWidth(3,50)
        self.myLayout.setColumnStretch(3,2)
        self.myLayout.setColumnMinimumWidth(4,50)
        self.myLayout.setColumnStretch(4,1)

        self.affichageAvion = GraphWidget(Vecteur(-0.5,-0.5),0.009,0,10,2,mddFlightData) #On commence en (--0.5,-0.5), a l'echelle 5mm par pix, la piste commence en 0 et fait 10m, l'avion fait 2m de long
        self.myLayout.addWidget(self.affichageAvion,0,0,5,4)

        self.affichageRawInput = _GraphicalRawInput(mddRawInput)
        self.myLayout.addWidget(self.affichageRawInput,0,4,3,1)
        
        self.userInput = QtWidgets.QWidget(self)
        self.myLayout.addWidget(self.userInput,3,4,2,1)
        self.userInputLayout = QtWidgets.QVBoxLayout(self.userInput)
        self.userInputComboBox = QtWidgets.QComboBox(self.userInput)
        self.userInputLayout.addWidget(self.userInputComboBox)
        self.userInputComboBox.addItems(["ScriptControl","PilotControl","AutoPilotControl"])

        self.userInputSliders = SliderControlWidget(self,"PilotControl")
        self.userInputLayout.addWidget(self.userInputSliders)
        self.userInputSliders.addSlider("Pitch",mddPilotInput.setPitch,-100,100)
        self.userInputSliders.addSlider("Flaps",mddPilotInput.setFlaps,0,100)
        self.userInputSliders.addSlider("Throttle",mddPilotInput.setThrottle,0,100)

        self.updateThread = _UpdateThread(self.mddFlightData,frequenceAffichage)
        self.updateThread.refreshPlease.connect(self.refresh)

    def startUpdateThread(self):
        self.updateThread.start()

    def stopUpdateThread(self):
        self.updateThread.stop()

    def refresh(self):
        self.affichageAvion.refresh()
        self.affichageRawInput.refresh()
