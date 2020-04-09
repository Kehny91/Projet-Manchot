import PyQt5
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sys
import time
import os
from FlightData import FlightData

from math import sqrt,cos,sin

class Vecteur:
    def __init__(self,x,z):
        self.x = x
        self.z = z
    def getX(self):
        return self.x

    def getZ(self):
        return self.z
    
    def __sub__(self,other):
        return Vecteur(self.x- other.x, self.z-other.z)

    def __add__(self,other):
        return Vecteur(self.x+other.x, self.z+other.z)

    def __mul__(self, scal):
        return Vecteur(self.x*scal, self.z*scal)

    def norm(self):
        return sqrt(self.x**2 + self.z**2)

    def unitaire(self):
        return self*(1.0/self.norm)

    def rotate(self, angle):
        return Vecteur(self.x*cos(angle) - self.z*sin(angle) , self.x*sin(angle) + self.z*cos(angle) )

    def withZmin(self, zMin):
        return Vecteur(self.x, max(zMin,self.z))

"""
La realPositionFenetre, correspond aux coordonnées vraies (pysiques) du coin inferieur gauche de la fenetre.
Le scale s'exprime en m/pix. Il donne combien de metre est representé par un pixel
Une flightData exprime la position du batiMoteur
"""
class GraphWidget(QtWidgets.QWidget):
    #PUBLIC
    def __init__(self, realPositionFenetre, scale, runwayXStart, runwayLength, planeLength, planeHeight):
        super().__init__()
        self.realPositionFenetre = realPositionFenetre
        self.scale = scale
        self.runwayXStart = runwayXStart
        self.runwayLength = runwayLength
        if (__name__=="__main__"):
            self.picture = Qt.QPixmap("../Sprites/DroneAjuste.png")
        else:
            self.picture = Qt.QPixmap("./IHM/Sprites/DroneAjuste.png")

        self.picture = self.picture.transformed(Qt.QTransform().scale(planeLength/1253.0/scale,planeLength/1253.0/scale))
        self.planeLength = planeLength
        self.planeHeight = planeHeight
        self.flightData = FlightData(Vecteur(0,0),Vecteur(0,0),0)
        pB = Vecteur(1220, -176)
        pC = Vecteur(626, -151) #negatif pour avoir Z vers le haut, contrairement au systeme de pixel
        self.zMin = -0.5

        self.B0_C0 = (pC - pB)*(planeLength/1253.0) #C'est le vecteur qui relie B a C lorsque theta vaut 0, dans les coordonnées réelles

    #PUBLIC
    def setFlightData(self,flightData):
        self.flightData = flightData

    #PUBLIC
    def setRealPositionFenetre(self, realPositionFenetre):
        self.realPositionFenetre = realPositionFenetre.withZmin(self.zMin)
    
    #PUBLIC
    def setRealPositionFenetreCenter(self, realPositionFenetreCenter):
        realWidth = self.width()*self.scale
        realHeight = self.height()*self.scale
        self.setRealPositionFenetre(realPositionFenetreCenter - Vecteur(realWidth/2,realHeight/2))

    #PUBLIC
    #update()

    #PRIVATE
    #Se referencer a point.png
    def _getCPosition(self, flightData):
        #Un flight data contient la position B
        return flightData.getPosAvion()+(self.B0_C0.rotate(flightData.getAssiette()))

    #PRIVATE
    def _realToPix(self,O_M):
        #TODO verifier que le vecteur est dans le referentiel absolu
        rpf_M = O_M-self.realPositionFenetre #vecteur realPositionFenetre -> M
        return (int(rpf_M.getX()/self.scale),self.height() - int(rpf_M.getZ()/self.scale) )

    #PRIVATE
    def _drawGround(self, painter):
        painter.setPen(Qt.QColor(0,255,0))
        painter.setBrush(Qt.QColor(0,255,0))
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
        pictureToDraw = self.picture.transformed(Qt.QTransform().rotateRadians(-flightData.getAssiette())) # - car le sens positif des widgt est le sens hroarie
        rect = pictureToDraw.rect()
        posPix = self._realToPix(self._getCPosition(flightData))
        rect.moveCenter(Qt.QPoint(posPix[0],posPix[1]))
        painter.drawPixmap(rect, pictureToDraw)
    
    #PRIVATE
    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)
        self._drawGround(qp)
        self._drawRunway(qp, self.runwayXStart, self.runwayLength)
        self._drawPlane(qp,self.flightData)
        qp.end()