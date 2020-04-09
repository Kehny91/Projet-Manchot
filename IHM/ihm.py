from Widgets.ControlSurfaceWidget import ControlSurfaceWidget
from Widgets.GraphWidget import GraphWidget,Vecteur
from Widgets.SliderControlWidget import SliderControlWidget
import PyQt5.QtWidgets as QtWidgets

class IHM(QtWidgets.QWidget):
    def __init__(self, mddFlightData, mddRawInput):
        super().__init__()
        self.myLayout = QtWidgets.QGridLayout(self)

        self.affichageAvion = GraphWidget(Vecteur(0,0),0.005,0,10,2,0.3)
        
        self.affichageGouvernes = QtWidgets.QWidget(self)

        self.inputs = QtWidgets.QWidget(self)