import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt
import PyQt5
from math import sin,pi,cos
import sys
import time
TORAD = pi/180.0
TODEG = 180.0/pi

def round(x):
    xi = int(x)
    if (x-xi>0.5):
        return xi+1
    else:
        return xi

class ControlSurfaceWidget(QtWidgets.QWidget):
    def __init__(self, parent, maxAngle,name,getterMDD):
        super().__init__(parent)
        self.getterMDD = getterMDD
        self.myLayout = QtWidgets.QGridLayout(self)
        self.labelName = QtWidgets.QLabel(name,self)
        self.labelAngle = QtWidgets.QLabel("0°",self)
        self.schema = _ControlSurfaceWidgetGraph(self,maxAngle)

        self.myLayout.addWidget(self.labelName,0,0,1,1)
        self.myLayout.addWidget(self.labelAngle,1,0,1,1)
        self.myLayout.addWidget(self.schema,0,1,2,1)

        self.myLayout.setColumnStretch(0,1)
        self.myLayout.setColumnStretch(1,3)


    def setPercent(self, percent):
        self.schema.setPercent(percent)
        self.labelAngle.setText(str(round(self.schema.angle*TODEG))+"°")

    def refresh(self):
        self.setPercent(self.getterMDD())


class _ControlSurfaceWidgetGraph(QtWidgets.QWidget):
    def __init__(self, parent, maxAngle):
        super().__init__(parent)
        self.maxAngle = maxAngle
        self.angle = 0
        if (__name__=="__main__"):
            self.fixe = Qt.QPixmap("../Sprites/fixe.png")
            self.aileron = Qt.QPixmap("../Sprites/aileron.png")
        else:
            self.fixe = Qt.QPixmap("./IHM/Sprites/fixe.png")
            self.aileron = Qt.QPixmap("./IHM/Sprites/aileron.png")

        rapport = min(self.width(),self.height()/sin(self.maxAngle))/self.fixe.width()

        self.fixe0 = self.fixe.transformed(Qt.QTransform().scale(rapport,rapport))
        self.rectFixe =  self.fixe0.rect()
        self.rectFixe.moveRight(self.width())
        self.rectFixe.moveTop(round((self.height() - self.rectFixe.height())/2))

        self.aileron0 = self.aileron.transformed(Qt.QTransform().scale(rapport,rapport))


    def resizeEvent(self, event):
        rapport = min(self.width(),self.height()/sin(self.maxAngle))/self.fixe.width()
        self.fixe0 = self.fixe.transformed(Qt.QTransform().scale(rapport,rapport))
        self.rectFixe =  self.fixe0.rect()
        self.rectFixe.moveRight(self.width())
        self.rectFixe.moveTop(round((self.height() - self.rectFixe.height())/2))

        self.aileron0 = self.aileron.transformed(Qt.QTransform().scale(rapport,rapport))


    """
    Pourcentage positif = gouverne vers le bas
    """
    def setPercent(self,percent):
        self.angle = percent*self.maxAngle
        self.update()

    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)

        aileron = self.aileron0.transformed(Qt.QTransform().rotateRadians(-self.angle))
        rectAileron = aileron.rect()
        rectAileron.moveCenter(self.rectFixe.center())
        qp.drawPixmap(self.rectFixe, self.fixe0)
        qp.drawPixmap(rectAileron, aileron)
        qp.end()