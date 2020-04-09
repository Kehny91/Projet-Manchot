from PyQt5 import QtWidgets
from PyQt5 import Qt

if __name__ == "__main__":
    class MDD:
        def pushValue(self, x):
            pass
else:
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
    def __init__(self, parent, name, outputMDD, mini, maxi):
        super().__init__(parent)
        self.outputMDD = outputMDD
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
        self.outputMDD.pushValue(x/100)

import sys
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = SliderControlWidget(mainW,"Pilot Input")
    mddPitch = MDD()
    mddFlaps = MDD()
    mddThrottle = MDD()

    graph.addSlider("Pitch",mddPitch,-100,100)
    graph.addSlider("Flaps",mddFlaps,0,100)
    graph.addSlider("Throttle",mddThrottle,0,100)

    mainW.setCentralWidget(graph)
    mainW.show()
    graph.update()
    sys.exit(app.exec_())