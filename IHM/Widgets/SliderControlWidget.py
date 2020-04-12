from PyQt5 import QtWidgets
from PyQt5 import Qt
from DataManagement import MDD
import PyQt5

class SliderControlWidget(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self._sliderUnits = []
        self._myLayout = QtWidgets.QHBoxLayout(self)

    def addSlider(self, name, MDDsetter, mini, maxi):
        newOne = _SliderUnit(self,name,MDDsetter,mini,maxi)
        self._sliderUnits.append(newOne)
        self._myLayout.addWidget(newOne)


class _SliderUnit(QtWidgets.QWidget):
    def __init__(self, parent, name, MDDsetter, mini, maxi):
        super().__init__(parent)
        self._MDDsetter = MDDsetter
        myLayout = QtWidgets.QVBoxLayout(self)
        self._labelName = QtWidgets.QLabel(name,self)
        self._labelOutput = QtWidgets.QLabel("0",self)
        self._slider = QtWidgets.QSlider(PyQt5.QtCore.Qt.Vertical,self)
        myLayout.addWidget(self._labelName)
        myLayout.addWidget(self._labelOutput)
        myLayout.addWidget(self._slider)

        self._slider.setMinimum(mini)
        self._slider.setMaximum(maxi)


        self._slider.valueChanged[int].connect(self._valueChanged)
        self._slider.setTickPosition(1)
        self._slider.setTickInterval(100)

    def _valueChanged(self, x):
        self._labelOutput.setText(str(x))
        self._MDDsetter(x/100)