import PyQt5
import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import sys
from Espace import Vecteur,Referentiel

"""
La realPositionFenetre, correspond aux coordonnées vraies (pysiques) du coin inferieur gauche de la fenetre.
Le scale s'exprime en m/pix. Il donne combien de metre est representé par un pixel
"""
class GraphWidget(QtWidgets.QWidget):
    def __init__(self, realPositionFenetre, scale):
        super().__init__()
        self.realPositionFenetre = realPositionFenetre
        self.scale = scale

    def _realToPix(self,O_M):
        #TODO verifier que le vecteur est dans le referentiel absolu
        rpf_M = O_M-self.realPositionFenetre #vecteur realPositionFenetre -> M
        return (int(rpf_M.getX()/self.scale),self.height() - int(rpf_M.getY()/self.scale) )
    
    def paintEvent(self, event):
        qp = Qt.QPainter()
        qp.begin(self)
        qp.setPen(Qt.QColor(0,0,0))
        qp.drawLine(0,0,self.width(),self.height())
        qp.end()

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    mainW.setCentralWidget(GraphWidget())
    mainW.show()
    sys.exit(app.exec_())