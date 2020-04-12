import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt
import PyQt5


class EngineWidget(QtWidgets.QWidget):
    def __init__(self, parent, maxThrust,name,getterMDD):
        super(EngineWidget,self).__init__(parent)
        self._getterMDD = getterMDD
        self._maxThrust = maxThrust
        myLayout = QtWidgets.QGridLayout(self)
        self._labelName = QtWidgets.QLabel(name,self)
        self._labelForce = QtWidgets.QLabel("0 N",self)
        self._schema = _EngineWidget()

        myLayout.addWidget(self._labelName,0,0,1,1)
        myLayout.addWidget(self._labelForce,1,0,1,1)
        myLayout.addWidget(self._schema,0,1,2,1)

        myLayout.setColumnStretch(0,1)
        myLayout.setColumnStretch(1,2)

    def setPercent(self, percent):
        self._labelForce.setText(str(round(self._maxThrust*percent*100)/100)+" N")

    def refresh(self):
        self.setPercent(self._getterMDD())

class _EngineWidget(QtWidgets.QWidget):
    def __init__(self):
        super(_EngineWidget,self).__init__()
        self._pictureRaw = Qt.QPixmap("./IHM/Sprites/moteur.png")
        rapport = min(self.width()/self._pictureRaw.width(),self.height()/self._pictureRaw.height())
        self._picture = self._pictureRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self._rectPicture =  self._picture.rect()
        self._rectPicture.moveCenter(Qt.QPoint(int(self.width()/2),int(self.height()/2)))

    def resizeEvent(self, event):
        rapport = min(self.width()/self._pictureRaw.width(),self.height()/self._pictureRaw.height())
        self._picture = self._pictureRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self._rectPicture =  self._picture.rect()
        self._rectPicture.moveCenter(Qt.QPoint(int(self.width()/2),int(self.height()/2)))

    def paintEvent(self,event):
        qp = Qt.QPainter()
        qp.begin(self)
        qp.drawPixmap(self._rectPicture, self._picture)
        qp.end()

