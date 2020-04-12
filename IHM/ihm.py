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
        myLayout = QtWidgets.QVBoxLayout(self)

        self._affFlapsG = ControlSurfaceWidget(self,ParametresModele.flapsGMaxAngle,"flapsG",mddRawInput.getFlapsG)
        myLayout.addWidget(self._affFlapsG)

        self._affFlapsD = ControlSurfaceWidget(self,ParametresModele.flapsDMaxAngle,"flapsD",mddRawInput.getFlapsD)
        myLayout.addWidget(self._affFlapsD)

        self._affElevG = ControlSurfaceWidget(self,ParametresModele.elevGMaxAngle,"elevG",mddRawInput.getElevG)
        myLayout.addWidget(self._affElevG)

        self._affElevD = ControlSurfaceWidget(self,ParametresModele.elevDMaxAngle,"elevD",mddRawInput.getElevD)
        myLayout.addWidget(self._affElevD)

        self._affEngine = EngineWidget(self,ParametresModele.engineMaxThrust,"engine", mddRawInput.getThrottle)
        myLayout.addWidget(self._affEngine)

    def refresh(self):
        self._affElevD.refresh()
        self._affElevG.refresh()
        self._affEngine.refresh()
        self._affFlapsD.refresh()
        self._affFlapsG.refresh()


class _InputWidget(QtWidgets.QWidget):
    def __init__(self,mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput):
        super(_InputWidget,self).__init__()
        self._mddMode = mddMode
        self._mddRawInput = mddRawInput
        self._mddPilotInput = mddPilotInput
        self._mddAutoPilotInput = mddAutoPilotInput

        myLayout = QtWidgets.QVBoxLayout(self)
        groupOfButtons = QtWidgets.QGroupBox(self)
        myLayout.addWidget(groupOfButtons)

        groupOfButtonsLayout = QtWidgets.QHBoxLayout()
        groupOfButtons.setLayout(groupOfButtonsLayout)

        self._buttonPilot = QtWidgets.QRadioButton("Pilot Input",self)
        self._buttonAutoPilot = QtWidgets.QRadioButton("Auto Pilot Input", self)
        self._buttonScript = QtWidgets.QRadioButton("Script Input",self)

        groupOfButtonsLayout.addWidget(self._buttonPilot)
        groupOfButtonsLayout.addWidget(self._buttonAutoPilot)
        groupOfButtonsLayout.addWidget(self._buttonScript)

        stack = QtWidgets.QStackedLayout()
        myLayout.addLayout(stack)

        #Pilot

        widget = SliderControlWidget(self)
        widget.addSlider("Pitch[%]",mddPilotInput.setPitch,-100,100)
        widget.addSlider("Flaps[%]",mddPilotInput.setFlaps,0,100)
        widget.addSlider("Throttle[%]",mddPilotInput.setThrottle,0,100)

        stack.addWidget(widget)

        #AutoPilot

        widget = SliderControlWidget(self)
        widget.addSlider("Vx[km/h]",mddAutoPilotInput.setVx,0,int(ParametresModele.maxAutoPilotSpeed*3.6))
        widget.addSlider("Vz[km/h]",mddAutoPilotInput.setVz,-int(ParametresModele.maxAutoPilotZSpeed*3.6),int(ParametresModele.maxAutoPilotZSpeed*3.6))

        stack.addWidget(widget)

        #Script

        widget = QtWidgets.QWidget(self)

        stack.addWidget(widget)

        self._buttonPilot.toggled.connect(lambda : stack.setCurrentIndex(0))
        self._buttonAutoPilot.toggled.connect(lambda : stack.setCurrentIndex(1))
        self._buttonScript.toggled.connect(lambda : stack.setCurrentIndex(2))

        stack.setCurrentIndex(0)
        self._buttonPilot.toggle()



class IHM(QtWidgets.QWidget):
    def __init__(self, mddFlightData, mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput, frequenceAffichage):
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
        
        self.userInput = _InputWidget(mddMode,mddRawInput,mddPilotInput,mddAutoPilotInput)
        self.myLayout.addWidget(self.userInput,3,4,2,1)

        self.updateThread = _UpdateThread(self.mddFlightData,frequenceAffichage)
        self.updateThread.refreshPlease.connect(self.refresh)

    def startUpdateThread(self):
        self.updateThread.start()

    def stopUpdateThread(self):
        self.updateThread.stop()

    def refresh(self):
        self.affichageAvion.refresh()
        self.affichageRawInput.refresh()
