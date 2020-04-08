import PyQt5
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sys
import time

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

"""
La realPositionFenetre, correspond aux coordonnées vraies (pysiques) du coin inferieur gauche de la fenetre.
Le scale s'exprime en m/pix. Il donne combien de metre est representé par un pixel
"""
class GraphWidget(QtWidgets.QWidget):
    def __init__(self, realPositionFenetre, scale, runwayXStart, runwayLength):
        super().__init__()
        self.realPositionFenetre = realPositionFenetre
        self.scale = scale
        self.runwayXStart = runwayXStart
        self.runwayLength = runwayLength

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
    
    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)
        self.drawGround(qp)
        self.drawRunway(qp, self.runwayXStart, self.runwayLength)
        qp.end()
    
    def setRealPositionFenetre(self, realPositionFenetre):
        self.realPositionFenetre = realPositionFenetre

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    mainW.setFixedWidth(500)
    mainW.setFixedHeight(500)
    mainW.setCentralWidget(GraphWidget(Vecteur(0,0),0.5, 5,15))
    mainW.show()
    for i in range(4000):
        mainW.centralWidget().setRealPositionFenetre(Vecteur(0,-i/100))
        mainW.centralWidget().update()
        Qt.QApplication.processEvents()
        time.sleep(0.001)
    sys.exit(app.exec_())