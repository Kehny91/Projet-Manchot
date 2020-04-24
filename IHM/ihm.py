from IHM.Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from IHM.Widgets.EngineWidget import EngineWidget
from IHM.Widgets.GraphWidget import GraphWidget
from IHM.Widgets.SliderControlWidget import SliderControlWidget
from IHM.Widgets.ValueWidget import ValueWidget
from Data.DataTypes import PilotInput,AutoPilotInput,RawInput
import PyQt5.QtWidgets as QtWidgets
import PyQt5
from Physique.Espace import Vecteur
from Parametres import ParametresModele,ParametresSimulation, ParametreMode
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

        self.stack = QtWidgets.QStackedLayout()
        myLayout.addLayout(self.stack)

        #Pilot

        widget = SliderControlWidget(self)

        iniPilotInput = mddPilotInput.read()
        slider = widget.addSlider("Pitch[%]",-100,100)
        slider._slider.setValue(int(iniPilotInput.getPitch()*100))
        slider.valueChanged[int].connect(lambda x : mddPilotInput.doOnData(PilotInput.setPitch,x/100))

        slider = widget.addSlider("Flaps[%]",0,100)
        slider._slider.setValue(int(iniPilotInput.getFlaps()*100))
        slider.valueChanged[int].connect(lambda x : mddPilotInput.doOnData(PilotInput.setFlaps,x/100))

        slider = widget.addSlider("Throttle[%]",0,100)
        slider._slider.setValue(int(iniPilotInput.getThrottle()*100))
        slider.valueChanged[int].connect(lambda x : mddPilotInput.doOnData(PilotInput.setThrottle,x/100))

        self.stack.addWidget(widget)

        #AutoPilot

        iniAutoPilotInput = mddAutoPilotInput.read()
        widget = SliderControlWidget(self)
        slider = widget.addSlider("Vx[km/h]",0,int(ParametresModele.maxAutoPilotSpeed*3.6))
        slider._slider.setValue(int(iniAutoPilotInput.getVx()*3.6))
        slider.valueChanged[int].connect(lambda x : mddAutoPilotInput.doOnData(AutoPilotInput.setVx,x/3.6))

        slider = widget.addSlider("Vz[km/h]",-int(ParametresModele.maxAutoPilotZSpeed*3.6),int(ParametresModele.maxAutoPilotZSpeed*3.6))
        slider._slider.setValue(int(iniAutoPilotInput.getVz()*3.6))
        slider.valueChanged[int].connect(lambda x : mddAutoPilotInput.doOnData(AutoPilotInput.setVz,x/3.6))

        self.stack.addWidget(widget)

        #Script

        widget = QtWidgets.QWidget(self)

        self.stack.addWidget(widget)

        self._buttonPilot.toggled.connect(lambda : self._handleRadioButton(0, mddMode,ParametreMode.MODE_PILOT))
        self._buttonAutoPilot.toggled.connect(lambda : self._handleRadioButton(1, mddMode,ParametreMode.MODE_AUTO_PILOT))
        self._buttonScript.toggled.connect(lambda : self._handleRadioButton(2, mddMode,ParametresSimulation.scriptToLoad.mode))
        

    def _handleRadioButton(self,index,mddMode,mode):
        mddMode.write(mode)
        time.sleep(0.3)
        self.stack.setCurrentIndex(index)
        if (index<2):
            self.stack.widget(index).refreshAllSliders()

    def artificiallyPressButton(self, mode):
        if (mode == ParametreMode.MODE_PILOT):
            self._buttonPilot.toggle()
        elif mode == ParametreMode.MODE_AUTO_PILOT:
            self._buttonAutoPilot.toggle()
        else:
            self._buttonScript.toggle()



class _TelemetryWidget(QtWidgets.QWidget):
    def __init__(self, mddFlightData, parent):
        super(_TelemetryWidget,self).__init__(parent)

        self._mddFlightData = mddFlightData

        myLayout = QtWidgets.QGridLayout(self)
        
        self._speedWidget = ValueWidget(self,"Speed","m/s",0)
        myLayout.addWidget(self._speedWidget,0,0)

        self._verticalSpeedWidget = ValueWidget(self,"VerticalSpeed","m/s",0)
        myLayout.addWidget(self._verticalSpeedWidget,1,0)

        self._assietteWidget = ValueWidget(self,"Assiette","°",0)
        myLayout.addWidget(self._assietteWidget,2,0)

        self._timeWidget = ValueWidget(self,"Time","s",0)
        myLayout.addWidget(self._timeWidget,0,1)

        self._posXWidget = ValueWidget(self,"posX","m",0)
        myLayout.addWidget(self._posXWidget,1,1)

        self._posZWidget = ValueWidget(self,"posZ","m",0)
        myLayout.addWidget(self._posZWidget,2,1)

    def refresh(self):
        fd = self._mddFlightData.read()
        self._speedWidget.setValue(fd.getVAvion().norm())
        self._speedWidget.refresh()

        self._verticalSpeedWidget.setValue(fd.getVAvion().getZ())
        self._verticalSpeedWidget.refresh()

        self._assietteWidget.setValue(fd.getAssiette()*TODEG)
        self._assietteWidget.refresh()

        self._timeWidget.setValue(fd.getTime())
        self._timeWidget.refresh()

        self._posXWidget.setValue(fd.getPosAvion().getX())
        self._posXWidget.refresh()

        self._posZWidget.setValue(fd.getPosAvion().getZ())
        self._posZWidget.refresh()





class IHM(QtWidgets.QWidget):
    def __init__(self, world, mddFlightData, mddMode, mddRawInput, mddPilotInput, mddAutoPilotInput, frequenceAffichage):
        super().__init__()
        self.world = world
        #self._mddFlightData = mddFlightData
        #self._mddRawInput = mddRawInput
        #self._mddMode = mddMode
        #self._mddAutoPilotInput  = mddAutoPilotInput
        #self._mddPilotInput = mddPilotInput


        myLayout = QtWidgets.QGridLayout(self)
        myLayout.setColumnMinimumWidth(0,150)
        myLayout.setColumnStretch(0,2)
        myLayout.setColumnMinimumWidth(1,150)
        myLayout.setColumnStretch(1,2)
        myLayout.setColumnMinimumWidth(2,150)
        myLayout.setColumnStretch(2,2)
        myLayout.setColumnMinimumWidth(3,150)
        myLayout.setColumnStretch(3,2)
        myLayout.setColumnMinimumWidth(4,50)
        myLayout.setColumnStretch(4,1)

        self._affichageAvion = GraphWidget(Vecteur(-0.5,-0.5),world.scale,world.positionPiste,world.taillePiste,ParametresModele.longueurDrone,mddFlightData, world) #On commence en (--0.5,-0.5), a l'echelle 5mm par pix, la piste commence en 0 et fait 10m, l'avion fait 2m de long
        myLayout.addWidget(self._affichageAvion,0,0,5,4)

        self._affichageRawInput = _GraphicalRawInput(mddRawInput)
        myLayout.addWidget(self._affichageRawInput,0,4,3,1)
        
        self._userInput = _InputWidget(mddMode,mddRawInput,mddPilotInput,mddAutoPilotInput)
        myLayout.addWidget(self._userInput,3,4,2,1)

        self._telemetry = _TelemetryWidget(mddFlightData,self)
        myLayout.addWidget(self._telemetry,5,0,1,5)

        self._updateThread = _UpdateThread(mddFlightData,frequenceAffichage)
        self._updateThread.refreshPlease.connect(self.refresh)

    def startUpdateThread(self):
        self._updateThread.start()

    def stopUpdateThread(self):
        self._updateThread.stop()

    def refresh(self):
        self._affichageAvion.refresh()
        self._affichageRawInput.refresh()
        self._telemetry.refresh()

    def artificiallyPressButton(self, mode):
        self._userInput.artificiallyPressButton(mode)
