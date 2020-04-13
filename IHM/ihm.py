from IHM.Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from IHM.Widgets.EngineWidget import EngineWidget
from IHM.Widgets.GraphWidget import GraphWidget
from IHM.Widgets.SliderControlWidget import SliderControlWidget
from DataTypes import PilotInput,AutoPilotInput,RawInput
import PyQt5.QtWidgets as QtWidgets
import PyQt5
from Test_IHM import Vecteur
from Parametres import ParametresModele
from PyQt5.QtCore import pyqtSignal,QObject
from PyQt5 import Qt
from math import pi
import time
import Modes as M
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
        self._mddRawInput = mddRawInput

        myLayout = QtWidgets.QVBoxLayout(self)

        self._affFlapsG = ControlSurfaceWidget(self,ParametresModele.flapsGMaxAngle,"flapsG")
        myLayout.addWidget(self._affFlapsG)

        self._affFlapsD = ControlSurfaceWidget(self,ParametresModele.flapsDMaxAngle,"flapsD")
        myLayout.addWidget(self._affFlapsD)

        self._affElevG = ControlSurfaceWidget(self,ParametresModele.elevGMaxAngle,"elevG")
        myLayout.addWidget(self._affElevG)

        self._affElevD = ControlSurfaceWidget(self,ParametresModele.elevDMaxAngle,"elevD")
        myLayout.addWidget(self._affElevD)

        self._affEngine = EngineWidget(self,ParametresModele.engineMaxThrust,"engine")
        myLayout.addWidget(self._affEngine)

    def refresh(self):
        rawInput = self._mddRawInput.read()
        self._affElevD.setPercent(rawInput.getElevD())
        self._affElevG.setPercent(rawInput.getElevG())
        self._affEngine.setPercent(rawInput.getThrottle())
        self._affFlapsD.setPercent(rawInput.getFlapsD())
        self._affFlapsG.setPercent(rawInput.getFlapsG())


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

        slider = widget.addSlider("Pitch[%]",-100,100)
        slider.valueChanged[int].connect(lambda x : mddPilotInput.doOnData(PilotInput.setPitch,x/100))

        slider = widget.addSlider("Flaps[%]",0,100)
        slider.valueChanged[int].connect(lambda x : mddPilotInput.doOnData(PilotInput.setFlaps,x/100))

        slider = widget.addSlider("Throttle[%]",0,100)
        slider.valueChanged[int].connect(lambda x : mddPilotInput.doOnData(PilotInput.setThrottle,x/100))

        stack.addWidget(widget)

        #AutoPilot

        widget = SliderControlWidget(self)
        slider = widget.addSlider("Vx[km/h]",0,int(ParametresModele.maxAutoPilotSpeed*3.6))
        slider.valueChanged[int].connect(lambda x : mddAutoPilotInput.doOnData(AutoPilotInput.setVx,x/3.6))

        slider = widget.addSlider("Vz[km/h]",-int(ParametresModele.maxAutoPilotZSpeed*3.6),int(ParametresModele.maxAutoPilotZSpeed*3.6))
        slider.valueChanged[int].connect(lambda x : mddAutoPilotInput.doOnData(AutoPilotInput.setVz,x/3.6))

        stack.addWidget(widget)

        #Script

        widget = QtWidgets.QWidget(self)

        stack.addWidget(widget)

        self._buttonPilot.toggled.connect(lambda : self._handleRadioButton(stack,0,mddMode,M.MODE_PILOT))
        self._buttonAutoPilot.toggled.connect(lambda : self._handleRadioButton(stack,1,mddMode,M.MODE_AUTO_PILOT))
        self._buttonScript.toggled.connect(lambda : self._handleRadioButton(stack,2,mddMode,M.MODE_SCRIPT_RAW))

        stack.setCurrentIndex(0)
        self._buttonPilot.toggle()

    def _handleRadioButton(self,stack,index,mddMode,mode):
        stack.setCurrentIndex(index)
        mddMode.write(mode)
        if (index<2):
            stack.widget(index).refreshAllSliders()



class IHM(QtWidgets.QWidget):
    def __init__(self, mddFlightData, mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput, frequenceAffichage):
        super().__init__()
        #self._mddFlightData = mddFlightData
        #self._mddRawInput = mddRawInput
        #self._mddMode = mddMode
        #self._mddAutoPilotInput  = mddAutoPilotInput
        #self._mddPilotInput = mddPilotInput


        myLayout = QtWidgets.QGridLayout(self)
        myLayout.setColumnMinimumWidth(0,50)
        myLayout.setColumnStretch(0,2)
        myLayout.setColumnMinimumWidth(1,50)
        myLayout.setColumnStretch(1,2)
        myLayout.setColumnMinimumWidth(2,50)
        myLayout.setColumnStretch(2,2)
        myLayout.setColumnMinimumWidth(3,50)
        myLayout.setColumnStretch(3,2)
        myLayout.setColumnMinimumWidth(4,50)
        myLayout.setColumnStretch(4,1)

        self._affichageAvion = GraphWidget(Vecteur(-0.5,-0.5),0.009,0,10,2,mddFlightData) #On commence en (--0.5,-0.5), a l'echelle 5mm par pix, la piste commence en 0 et fait 10m, l'avion fait 2m de long
        myLayout.addWidget(self._affichageAvion,0,0,5,4)

        self._affichageRawInput = _GraphicalRawInput(mddRawInput)
        myLayout.addWidget(self._affichageRawInput,0,4,3,1)
        
        self._userInput = _InputWidget(mddMode,mddRawInput,mddPilotInput,mddAutoPilotInput)
        myLayout.addWidget(self._userInput,3,4,2,1)

        self._updateThread = _UpdateThread(mddFlightData,frequenceAffichage)
        self._updateThread.refreshPlease.connect(self.refresh)

    def startUpdateThread(self):
        self._updateThread.start()

    def stopUpdateThread(self):
        self._updateThread.stop()

    def refresh(self):
        self._affichageAvion.refresh()
        self._affichageRawInput.refresh()
