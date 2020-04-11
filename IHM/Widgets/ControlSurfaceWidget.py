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
        self.myLayout.setColumnStretch(1,2)


    def setPercent(self, percent):
        self.schema.setPercent(percent)
        self.labelAngle.setText(str(round(self.schema.angle*TODEG))+"°")

    #Fait aussi l'update via la methode setPercent
    def refresh(self):
        self.setPercent(self.getterMDD())


class _ControlSurfaceWidgetGraph(QtWidgets.QWidget):
    def __init__(self, parent, maxAngle):
        super().__init__(parent)
        self.maxAngle = maxAngle
        self.angle = 0
        self.pictureStabRaw = Qt.QPixmap("./IHM/Sprites/stab.png")
        self.pictureGouverneRaw = Qt.QPixmap("./IHM/Sprites/gouverne.png")

        rapport = min(self.height()/self.pictureStabRaw.height(),
                        min(self.width()/self.pictureStabRaw.width(),self.height()/(sin(self.maxAngle)*self.pictureStabRaw.width()))
        )

        self.pictureStab0 = self.pictureStabRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self.pictureGouverne0 = self.pictureGouverneRaw.transformed(Qt.QTransform().scale(rapport,rapport))

        self.rectStab =  self.pictureStab0.rect()
        self.rectStab.moveRight(self.width())
        self.rectStab.moveTop(round((self.height() - self.rectStab.height())/2))

        #Le rect de la gouverne doit lui etre recalcule a chaque fois

        


    def resizeEvent(self, event):
        rapport = min(self.height()/self.pictureStabRaw.height(),
                        min(self.width()/self.pictureStabRaw.width(),self.height()/(sin(self.maxAngle)*self.pictureStabRaw.width()))
        )
        self.pictureStab0 = self.pictureStabRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self.pictureGouverne0 = self.pictureGouverneRaw.transformed(Qt.QTransform().scale(rapport,rapport))

        self.rectStab =  self.pictureStab0.rect()
        self.rectStab.moveRight(self.width())
        self.rectStab.moveTop(round((self.height() - self.rectStab.height())/2))


    """
    Pourcentage positif = gouverne vers le bas
    """
    def setPercent(self,percent):
        self.angle = percent*self.maxAngle
        self.update()

    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)

        pictureGouverne = self.pictureGouverne0.transformed(Qt.QTransform().rotateRadians(-self.angle))
        rectGouverne = pictureGouverne.rect()
        rectGouverne.moveCenter(self.rectStab.center())
        qp.drawPixmap(self.rectStab, self.pictureStab0)
        qp.drawPixmap(rectGouverne, pictureGouverne)
        qp.end()