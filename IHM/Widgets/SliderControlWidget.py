from PyQt5 import QtWidgets
from PyQt5 import Qt
from DataManagement import MDD
import PyQt5

class SliderControlWidget(QtWidgets.QWidget):
    def __init__(self,parent,name):
        super().__init__(parent)
        self.sliderUnits = []
        self.myLayout = QtWidgets.QVBoxLayout(self)
        self.myLayout.addWidget(QtWidgets.QLabel("Pilot Input",self))
        self.insiderLayout = QtWidgets.QHBoxLayout()
        self.myLayout.addLayout(self.insiderLayout)

    def addSlider(self, name, mdd, mini, maxi):
        newOne = _SliderUnit(self,name,mdd,mini,maxi)
        self.sliderUnits.append(newOne)
        self.insiderLayout.addWidget(newOne)


class _SliderUnit(QtWidgets.QWidget):
    def __init__(self, parent, name, MDDsetter, mini, maxi):
        super().__init__(parent)
        self.MDDsetter = MDDsetter
        self.myLayout = QtWidgets.QVBoxLayout(self)
        self.labelName = QtWidgets.QLabel(name,self)
        self.labelOutput = QtWidgets.QLabel("0",self)
        self.slider = QtWidgets.QSlider(PyQt5.QtCore.Qt.Vertical,self)
        self.myLayout.addWidget(self.labelName)
        self.myLayout.addWidget(self.labelOutput)
        self.myLayout.addWidget(self.slider)

        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)


        self.slider.valueChanged[int].connect(self._valueChanged)
        self.slider.setTickPosition(1)
        self.slider.setTickInterval(100)

    def _valueChanged(self, x):
        self.labelOutput.setText(str(x))
        self.MDDsetter(x/100)