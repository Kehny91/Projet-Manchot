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
        self._getterMDD = getterMDD
        myLayout = QtWidgets.QGridLayout(self)
        self._labelName = QtWidgets.QLabel(name,self)
        self._labelAngle = QtWidgets.QLabel("0°",self)
        self._schema = _ControlSurfaceWidgetGraph(self,maxAngle)

        myLayout.addWidget(self._labelName,0,0,1,1)
        myLayout.addWidget(self._labelAngle,1,0,1,1)
        myLayout.addWidget(self._schema,0,1,2,1)

        myLayout.setColumnStretch(0,1)
        myLayout.setColumnStretch(1,2)


    def setPercent(self, percent):
        self._schema.setPercent(percent)
        self._labelAngle.setText(str(round(self._schema.getAngle()*TODEG))+"°")

    #Fait aussi l'update via la methode setPercent
    def refresh(self):
        self.setPercent(self._getterMDD())


class _ControlSurfaceWidgetGraph(QtWidgets.QWidget):
    def __init__(self, parent, maxAngle):
        super().__init__(parent)
        self._maxAngle = maxAngle
        self._angle = 0
        self._pictureStabRaw = Qt.QPixmap("./IHM/Sprites/stab.png")
        self._pictureGouverneRaw = Qt.QPixmap("./IHM/Sprites/gouverne.png")

        rapport = min(self.height()/self._pictureStabRaw.height(),
                        min(self.width()/self._pictureStabRaw.width(),self.height()/(sin(self._maxAngle)*self._pictureStabRaw.width()))
        )

        self._pictureStab0 = self._pictureStabRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self._pictureGouverne0 = self._pictureGouverneRaw.transformed(Qt.QTransform().scale(rapport,rapport))

        self._rectStab =  self._pictureStab0.rect()
        self._rectStab.moveRight(self.width())
        self._rectStab.moveTop(round((self.height() - self._rectStab.height())/2))

        #Le rect de la gouverne doit lui etre recalcule a chaque fois

        


    def resizeEvent(self, event):
        rapport = min(self.height()/self._pictureStabRaw.height(),
                        min(self.width()/self._pictureStabRaw.width(),self.height()/(sin(self._maxAngle)*self._pictureStabRaw.width()))
        )

        self._pictureStab0 = self._pictureStabRaw.transformed(Qt.QTransform().scale(rapport,rapport))
        self._pictureGouverne0 = self._pictureGouverneRaw.transformed(Qt.QTransform().scale(rapport,rapport))

        self._rectStab =  self._pictureStab0.rect()
        self._rectStab.moveRight(self.width())
        self._rectStab.moveTop(round((self.height() - self._rectStab.height())/2))


    """
    Pourcentage positif = gouverne vers le bas
    """
    def setPercent(self,percent):
        self._angle = percent*self._maxAngle
        self.update()

    def getAngle(self):
        return self._angle

    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)

        pictureGouverne = self._pictureGouverne0.transformed(Qt.QTransform().rotateRadians(-self._angle))
        rectGouverne = pictureGouverne.rect()
        rectGouverne.moveCenter(self._rectStab.center())
        qp.drawPixmap(self._rectStab, self._pictureStab0)
        qp.drawPixmap(rectGouverne, pictureGouverne)
        qp.end()