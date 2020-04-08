import PyQt5
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sys
import time
import os

class FlightData:
    def __init__(self, posAvion, vAvion, assiette):
        self._posAvion = posAvion
        self._vAvion = vAvion
        self._assiette = assiette

    def getPosAvion(self):
        return self._posAvion

    def getVAvion(self):
        return self._vAvion

    def getAssiette(self):
        return self._assiette

    def setPosAvion(self, posAvion):
        self._posAvion = posAvion

    def setVAvion(self,vAvion):
        self._vAvion = vAvion

    def setAssiette(self, assiette):
        self._assiette = assiette

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

"""
La realPositionFenetre, correspond aux coordonnées vraies (pysiques) du coin inferieur gauche de la fenetre.
Le scale s'exprime en m/pix. Il donne combien de metre est representé par un pixel
"""
class GraphWidget(QtWidgets.QWidget):
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
        self.planeLength = planeLength
        self.planeHeight = planeHeight
        self.flightData = FlightData(Vecteur(0,0),Vecteur(0,0),0)

    def setFlightData(self,flightData):
        self.flightData = flightData

    def _realToPix(self,O_M):
        #TODO verifier que le vecteur est dans le referentiel absolu
        rpf_M = O_M-self.realPositionFenetre #vecteur realPositionFenetre -> M
        return (int(rpf_M.getX()/self.scale),self.height() - int(rpf_M.getZ()/self.scale) )

    def drawGround(self, painter):
        painter.setPen(Qt.QColor(0,255,0))
        painter.setBrush(Qt.QColor(0,255,0))
        pixPos = self._realToPix(Vecteur(0,0))
        painter.drawRect(0,max(pixPos[1],0),self.width(), self.height())

    def drawRunway(self, painter, xStart,longueur):
        painter.setPen(Qt.QColor(100,100,100))
        painter.setBrush(Qt.QColor(100,100,100))
        pixPosStart = self._realToPix(Vecteur(xStart,0))
        pixPosEnd = self._realToPix(Vecteur(xStart+longueur,-1))
        painter.drawRect(pixPosStart[0],pixPosStart[1],pixPosEnd[0] - pixPosStart[0], max(1,pixPosEnd[1] - pixPosStart[1]))

    def drawPlane(self, painter, flightData):
        rect = Qt.QRect()
        rect.setHeight(self.planeHeight/self.scale)
        rect.setWidth(self.planeLength/self.scale)
        posPix = self._realToPix(flightData.getPosAvion())
        rect.moveCenter(Qt.QPoint(posPix[0],posPix[1]))
        painter.drawPixmap(rect, self.picture, self.picture.rect())
    
    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)
        self.drawGround(qp)
        self.drawRunway(qp, self.runwayXStart, self.runwayLength)
        self.drawPlane(qp,self.flightData)
        qp.end()
    
    def setRealPositionFenetre(self, realPositionFenetre):
        self.realPositionFenetre = realPositionFenetre
    
    def setRealPositionFenetreCenter(self, realPositionFenetreCenter):
        realWidth = self.width()*self.scale
        realHeight = self.height()*self.scale
        self.setRealPositionFenetre(realPositionFenetreCenter - Vecteur(realWidth/2,realHeight/2))


class Updater(Qt.QThread):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
    
    def run(self):
        flightData = FlightData(Vecteur(0,3),Vecteur(0,0),0.0)
        while True:
            flightData.setPosAvion(flightData.getPosAvion()+Vecteur(0.015,-0.002))
            self.graph.setFlightData(flightData)
            self.graph.setRealPositionFenetreCenter(flightData.getPosAvion())
            self.graph.update()
            time.sleep(0.01)



if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    mainW.setFixedWidth(500)
    mainW.setFixedHeight(500)
    graph = GraphWidget(Vecteur(0,-1),0.03, 5,15,1.80,0.30)
    mainW.setCentralWidget(graph)
    mainW.show()
    updater = Updater(graph)
    updater.start()
    sys.exit(app.exec_())