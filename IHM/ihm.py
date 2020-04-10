from IHM.Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from IHM.Widgets.GraphWidget import GraphWidget
from IHM.Widgets.SliderControlWidget import SliderControlWidget
import PyQt5.QtWidgets as QtWidgets
import PyQt5
from Test_IHM import Vecteur

from math import pi
TORAD = pi/180.0
TODEG = 180.0/pi

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

        self.affichageGouvernes = QtWidgets.QWidget(self)
        self.myLayout.addWidget(self.affichageGouvernes,0,4,3,1)
        self.affichageGouvernesLayout = QtWidgets.QVBoxLayout(self.affichageGouvernes)
        self.flapsGAff = ControlSurfaceWidget(self.affichageGouvernes,45*TORAD,"flapsG",self.mddRawInput.getFlapsG)
        self.flapsDAff = ControlSurfaceWidget(self.affichageGouvernes,45*TORAD,"flapsD",self.mddRawInput.getFlapsD)
        self.elevGAff = ControlSurfaceWidget(self.affichageGouvernes,45*TORAD,"elevG",self.mddRawInput.getElevG)
        self.elevDAff = ControlSurfaceWidget(self.affichageGouvernes,45*TORAD,"elevD",self.mddRawInput.getElevD)
        self.affichageGouvernesLayout.addWidget(self.flapsDAff)
        self.affichageGouvernesLayout.addWidget(self.flapsGAff)
        self.affichageGouvernesLayout.addWidget(self.elevDAff)
        self.affichageGouvernesLayout.addWidget(self.elevGAff)
        
        self.userInput = QtWidgets.QWidget(self)
        self.myLayout.addWidget(self.userInput,3,4,2,1)
        self.userInputLayout = QtWidgets.QVBoxLayout(self.userInput)
        self.userInputComboBox = QtWidgets.QComboBox(self.userInput)
        self.userInputLayout.addWidget(self.userInputComboBox)
        self.userInputComboBox.addItems(["ScriptControl","PilotControl","AutoPilotControl"])

        self.userInputSliders = SliderControlWidget(self.affichageGouvernes,"PilotControl")
        self.userInputLayout.addWidget(self.userInputSliders)
        self.userInputSliders.addSlider("Pitch",mddPilotInput.setPitch,-100,100)
        self.userInputSliders.addSlider("Flaps",mddPilotInput.setFlaps,0,100)
        self.userInputSliders.addSlider("Throttle",mddPilotInput.setThrottle,0,100)

    def refresh(self):
        self.affichageAvion.refresh()
        self.flapsGAff.refresh()
        self.flapsDAff.refresh()
        self.elevDAff.refresh()
        self.elevGAff.refresh()
