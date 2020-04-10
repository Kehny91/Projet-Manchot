from IHM.ihm import IHM
from FlightData import MDDFlightData
from Espace import Vecteur

if __name__ == "__main__":

    mddFlightData = MDDFlightData(Vecteur()

    app = Qt.QApplication(sys.argv)
    mainW = Qt.QMainWindow()
    graph = IHM()
    mainW.setCentralWidget(graph)
    mainW.show()
    graph.update()
    u = updater(graph)
    u.start()
    sys.exit(app.exec_())