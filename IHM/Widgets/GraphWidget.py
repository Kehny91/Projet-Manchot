import PyQt5
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sys
import time
import os
from Espace import Vecteur,ReferentielAbsolu,moduloF
from math import sqrt,cos,sin
from DataTypes import Obstacle,Sol
from Solide import refSol

"""
La realPositionFenetre, correspond aux coordonnées vraies (pysiques) du coin inferieur gauche de la fenetre.
Le scale s'exprime en m/pix. Il donne combien de metre est representé par un pixel
Une flightData exprime la position du batiMoteur
"""
class GraphWidget(QtWidgets.QWidget):
    #PUBLIC
    def __init__(self, realPositionFenetre, scale, runwayXStart, runwayLength, planeLength, flightDataMDD, world):
        super().__init__()
        self._world = world
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
        self.setRealPositionFenetre(realPositionFenetreCenter.changeRef(ReferentielAbsolu()) - Vecteur(realWidth/2,realHeight/2))

    #PRIVATE
    #Se referencer a point.png
    def _getCPosition(self,flightData):
        #Un flight data contient la position B
        #TODO Utilisation de ref ?
        posAvion = flightData.getPosAvion()
        return posAvion + (self._B0_C0.rotate(flightData.getAssiette())).projectionRef(posAvion.getRef())

    #PRIVATE
    def _realToPix(self,O_M):
        #TODO verifier que le vecteur est dans le referentiel absolu
        rpf_M = O_M.changeRef(ReferentielAbsolu())-self._realPositionFenetre #vecteur realPositionFenetre -> M
        return (int(rpf_M.getX()/self._scale),self.height() - int(rpf_M.getZ()/self._scale) )

    #PRIVATE
    #Ground and sky
    def _drawGround(self, painter):
        #Le ground est en deux couleurs qui s'alterne
        tailleBande = 1 #m
        realWidthScreen = self.width()*self._scale
        limite =  self.width() - moduloF(self._realPositionFenetre.getX(),realWidthScreen+tailleBande)/self._scale

        #Sky
        painter.setPen(Qt.QColor(28, 98, 230))
        painter.setBrush(Qt.QColor(28, 98, 230))
        painter.drawRect(0,0,self.width(), self.height())

        #Ground
        painter.setPen(Qt.QColor(21, 173, 21))
        painter.setBrush(Qt.QColor(21, 173, 21))
        pixPos = self._realToPix(Vecteur(0,0))
        painter.drawRect(0,max(pixPos[1],0),self.width(), self.height())
        painter.setPen(Qt.QColor(21, 255, 21))
        painter.setBrush(Qt.QColor(21, 255, 21))
        painter.drawRect(limite,max(pixPos[1],0),tailleBande/self._scale, self.height())

        #Obstacles
        for obs in self._world.obstacles:
            if type(obs)!=type(Sol(refSol)):
                bg = self._realToPix(obs.pointBG)
                hd = self._realToPix(obs.pointHD)
                painter.setPen(Qt.QColor(21, 23, 56))
                painter.setBrush(Qt.QColor(21, 23, 56))
                painter.drawRect(bg[0],bg[1], hd[0] - bg[0], hd[1] - bg[1])


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