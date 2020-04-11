from IHM.Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from IHM.Widgets.EngineWidget import EngineWidget
from IHM.Widgets.GraphWidget import GraphWidget
from IHM.Widgets.SliderControlWidget import SliderControlWidget
import PyQt5.QtWidgets as QtWidgets
import PyQt5
from Test_IHM import Vecteur
from Parametres import ParametresModele
from math import pi
TORAD = pi/180.0
TODEG = 180.0/pi

class _GraphicalRawInput(QtWidgets.QWidget):
    def __init__(self,mddRawInput):
        super(_GraphicalRawInput,self).__init__()
        self.myLayout = QtWidgets.QVBoxLayout(self)

        self.affFlapsG = ControlSurfaceWidget(self,ParametresModele.flapsGMaxAngle,"flapsG",mddRawInput.getFlapsG)
        self.myLayout.addWidget(self.affFlapsG)

        self.affFlapsD = ControlSurfaceWidget(self,ParametresModele.flapsDMaxAngle,"flapsD",mddRawInput.getFlapsD)
        self.myLayout.addWidget(self.affFlapsD)

        self.affElevG = ControlSurfaceWidget(self,ParametresModele.elevGMaxAngle,"elevG",mddRawInput.getElevG)
        self.myLayout.addWidget(self.affElevG)

        self.affElevD = ControlSurfaceWidget(self,ParametresModele.elevDMaxAngle,"elevD",mddRawInput.getElevD)
        self.myLayout.addWidget(self.affElevD)

        self.affEngine = EngineWidget(self,ParametresModele.engineMaxThrust,"engine", mddRawInput.getThrottle)
        self.myLayout.addWidget(self.affEngine)

    def refresh(self):
        self.affElevD.refresh()
        self.affElevG.refresh()
        self.affEngine.refresh()
        self.affFlapsD.refresh()
        self.affFlapsG.refresh()


class IHM(QtWidgets.QWidget):
    def __init__(self, mddFlightData, mddRawInput, mddMode, mddAutoPilotInput, mddPilotInput):
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

    def refresh(self):
        self.affichageAvion.refresh()
        self.affichageRawInput.refresh()
