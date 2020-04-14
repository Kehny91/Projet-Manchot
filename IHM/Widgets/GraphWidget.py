import PyQt5
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sys
import time
import os
from Espace import Vecteur
from math import sqrt,cos,sin

"""
La realPositionFenetre, correspond aux coordonnées vraies (pysiques) du coin inferieur gauche de la fenetre.
Le scale s'exprime en m/pix. Il donne combien de metre est representé par un pixel
Une flightData exprime la position du batiMoteur
"""
class GraphWidget(QtWidgets.QWidget):
    #PUBLIC
    def __init__(self, realPositionFenetre, scale, runwayXStart, runwayLength, planeLength, flightDataMDD):
        super().__init__()
        self._zMin = -0.5
        self._realPositionFenetre = realPositionFenetre
        self.setRealPositionFenetre(realPositionFenetre)
        self._scale = scale
        self._runwayXStart = runwayXStart
        self._runwayLength = runwayLength
        if (__name__=="__main__"):
            self._picture = Qt.QPixmap("../Sprites/DroneAjuste.png")
        else:
            self._picture = Qt.QPixmap("./IHM/Sprites/DroneAjuste.png")

        self._picture = self._picture.transformed(Qt.QTransform().scale(planeLength/1253.0/scale,planeLength/1253.0/scale))

        self._flightDataMDD = flightDataMDD

        #TODO utilisation des referentiels ?
        self._B0_C0 = Vecteur((626-1220)/1253.0*planeLength,(176-115)/229.0*planeLength*229/1253) #C'est le vecteur qui relie B a C lorsque theta vaut 0, dans les coordonnées réelles

    def refresh(self):
        self.update()

    #PUBLIC
    def setRealPositionFenetre(self, realPositionFenetre):
        self._realPositionFenetre = realPositionFenetre.withZmin(self._zMin)
    
    #PUBLIC
    def setRealPositionFenetreCenter(self, realPositionFenetreCenter):
        realWidth = self.width()*self._scale
        realHeight = self.height()*self._scale
        self.setRealPositionFenetre(realPositionFenetreCenter - Vecteur(realWidth/2,realHeight/2))

    #PRIVATE
    #Se referencer a point.png
    def _getCPosition(self,flightData):
        #Un flight data contient la position B
        #TODO Utilisation de ref ?
        return flightData.getPosAvion()+(self._B0_C0.rotate(flightData.getAssiette()))

    #PRIVATE
    def _realToPix(self,O_M):
        #TODO verifier que le vecteur est dans le referentiel absolu
        rpf_M = O_M-self._realPositionFenetre #vecteur realPositionFenetre -> M
        return (int(rpf_M.getX()/self._scale),self.height() - int(rpf_M.getZ()/self._scale) )

    #PRIVATE
    #Ground and sky
    def _drawGround(self, painter):
        painter.setPen(Qt.QColor(28, 98, 230))
        painter.setBrush(Qt.QColor(28, 98, 230))
        painter.drawRect(0,0,self.width(), self.height())
        painter.setPen(Qt.QColor(21, 173, 21))
        painter.setBrush(Qt.QColor(21, 173, 21))
        pixPos = self._realToPix(Vecteur(0,0))
        painter.drawRect(0,max(pixPos[1],0),self.width(), self.height())

    #PRIVATE
    def _drawRunway(self, painter, xStart,longueur):
        painter.setPen(Qt.QColor(100,100,100))
        painter.setBrush(Qt.QColor(100,100,100))
        pixPosStart = self._realToPix(Vecteur(xStart,0))
        pixPosEnd = self._realToPix(Vecteur(xStart+longueur,-1))
        painter.drawRect(pixPosStart[0],pixPosStart[1],pixPosEnd[0] - pixPosStart[0], max(1,pixPosEnd[1] - pixPosStart[1]))

    #PRIVATE
    def _drawPlane(self, painter, flightData):
        pictureToDraw = self._picture.transformed(Qt.QTransform().rotateRadians(flightData.getAssiette()))
        rect = pictureToDraw.rect()
        posPix = self._realToPix(self._getCPosition(flightData))
        rect.moveCenter(Qt.QPoint(posPix[0],posPix[1]))
        painter.drawPixmap(rect, pictureToDraw)
    
    #PRIVATE
    def paintEvent(self, event):
        flightData = self._flightDataMDD.read()
        qp = Qt.QPainter()
        qp.begin(self)
        self.setRealPositionFenetreCenter(flightData.getPosAvion())
        self._drawGround(qp)
        self._drawRunway(qp, self._runwayXStart, self._runwayLength)
        self._drawPlane(qp,flightData)
        qp.end()