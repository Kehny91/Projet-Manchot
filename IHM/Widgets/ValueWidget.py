import PyQt5.QtWidgets as QtWidgets
from Logger import formatFloat

class ValueWidget(QtWidgets.QFrame):
    def __init__(self, parent, name, unit, value0):
        super(ValueWidget,self).__init__(parent)
        self._name = name
        self._unit = unit
        self._value = formatFloat(value0)

        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        myLayout = QtWidgets.QHBoxLayout(self)

        nameLabel = QtWidgets.QLabel(name,parent=self)
        myLayout.addWidget(nameLabel)

        self._valueLabel = QtWidgets.QLabel(self._value,parent=self)
        myLayout.addWidget(self._valueLabel)

        unitLabel = QtWidgets.QLabel(unit,parent=self)
        myLayout.addWidget(unitLabel)

    def setValue(self, value):
        self._value = formatFloat(value)

    def refresh(self):
        self._valueLabel.setText(self._value)