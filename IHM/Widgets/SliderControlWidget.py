from PyQt5 import QtWidgets
from PyQt5 import Qt
from DataManagement import MDD
import PyQt5

class SliderControlWidget(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self._sliderUnits = []
        self._myLayout = QtWidgets.QHBoxLayout(self)

    """Ajoute un slider et le renvoie"""
    def addSlider(self, name, mini, maxi):
        newOne = SliderUnit(self,name,mini,maxi)
        self._sliderUnits.append(newOne)
        self._myLayout.addWidget(newOne)
        return newOne

    def refreshAllSliders(self):
        for s in self._sliderUnits:
            s.refresh()


class SliderUnit(QtWidgets.QWidget):
    def __init__(self, parent, name, mini, maxi):
        super().__init__(parent)
        myLayout = QtWidgets.QVBoxLayout(self)
        self._labelName = QtWidgets.QLabel(name,self)
        self._labelOutput = QtWidgets.QLabel("0",self)
        self._slider = QtWidgets.QSlider(PyQt5.QtCore.Qt.Vertical,self)
        self.valueChanged = self._slider.valueChanged

        myLayout.addWidget(self._labelName)
        myLayout.addWidget(self._labelOutput)
        myLayout.addWidget(self._slider)

        self._slider.setMinimum(mini)
        self._slider.setMaximum(maxi)
        self._slider.setTickPosition(1)
        self._slider.setTickInterval(100)

        self._slider.valueChanged[int].connect(self.setLabelOutputTo)

    def refresh(self):
        self.valueChanged.emit(self._slider.value())

    def setLabelOutputTo(self, x):
        self._labelOutput.setText(str(x))