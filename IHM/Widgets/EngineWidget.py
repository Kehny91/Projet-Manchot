import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt
import PyQt5


class EngineWidget(QtWidgets.QWidget):
    def __init__(self, parent, maxThrust,name,getterMDD):
        super(EngineWidget,self).__init__(parent)
        self.getterMDD = getterMDD
        self.maxThrust = maxThrust
        self.myLayout = QtWidgets.QGridLayout(self)
        self.labelName = QtWidgets.QLabel(name,self)
        self.labelForce = QtWidgets.QLabel("0 N",self)
        self.schema = _EngineWidget()

        self.myLayout.addWidget(self.labelName,0,0,1,1)
        self.myLayout.addWidget(self.labelForce,1,0,1,1)
        self.myLayout.addWidget(self.schema,0,1,2,1)

        self.myLayout.setColumnStretch(0,1)
        self.myLayout.setColumnStretch(1,2)
        self.myLayout.setAlignment


    def setPercent(self, percent):
        self.labelForce.setText(str(round(self.maxThrust*percent*100)/100)+" N")

    def refresh(self):
        self.setPercent(self.getterMDD())

class _EngineWidget(QtWidgets.QWidget):
    def __init__(self):
        super(_EngineWidget,self).__init__()
        self.pictureRaw = Qt.QPixmap("./IHM/Sprites/moteur.png")
        rapport = min(self.width()/self.pictureRaw.width(),self.height()/self.pictureRaw.height())
        self.picture = self.pictureRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self.rectPicture =  self.picture.rect()
        self.rectPicture.moveCenter(Qt.QPoint(int(self.width()/2),int(self.height()/2)))

    def resizeEvent(self, event):
        rapport = min(self.width()/self.pictureRaw.width(),self.height()/self.pictureRaw.height())
        self.picture = self.pictureRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self.rectPicture =  self.picture.rect()
        self.rectPicture.moveCenter(Qt.QPoint(int(self.width()/2),int(self.height()/2)))

    def paintEvent(self,event):
        qp = Qt.QPainter()
        qp.begin(self)
        qp.drawPixmap(self.rectPicture, self.picture)
        qp.end()

