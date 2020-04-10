from Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from Widgets.GraphWidget import GraphWidget,Vecteur
from Widgets.SliderControlWidget import SliderControlWidget
import PyQt5.QtWidgets as QtWidgets

class IHM(QtWidgets.QWidget):
    def __init__(self, mddFlightData, mddRawInput, mddMode, mddAutoPilotInput, mddPilotInput):
        super().__init__()
        self.mddFlightData = mddFlightData
        self.mddRawInput = mddRawInput
        self.mddMode = mddMode
        self.mddAutoPilotInput  = mddAutoPilotInput
        self.mddPilotInput = mddPilotInput


        self.myLayout = QtWidgets.QGridLayout(self)

        self.affichageAvion = GraphWidget(Vecteur(0,0),0.005,0,10,2,0.3) #On commence en (0,0), a l'echelle 5mm par pix, la piste commence en 0 et fait 10m, l'avion fait 2m de long et 30cm de haut
        
        self.affichageGouvernes = QtWidgets.QWidget(self)
        self.affichageGouvernesLayout = QtWidgets.QVBoxLayout(self.affichageGouvernes)
        
        self.affichageGouvernesComboBox = QtWidgets.QComboBox(self.affichageGouvernesLayout)
        self.affichageGouvernesComboBox.addAction("ScriptControl")
        self.affichageGouvernesComboBox.addAction("PilotControl")
        self.affichageGouvernesComboBox.addAction("AutoPilotControl")

        self.affichageGouvernesSliders = SliderControlWidget(self.affichageGouvernesLayout,"PilotControl")
        self.affichageGouvernesSliders.addSlider("Pitch",mddPilotInput.mddPitch,-100,100)
        self.affichageGouvernesSliders.addSlider("Flaps",mddPilotInput.mddFlaps,0,100)
        self.affichageGouvernesSliders.addSlider("Throttle",mddPilotInput.mddThrottle,0,100)

        self.inputs = QtWidgets.QWidget(self)