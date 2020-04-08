import os.path as path
import os
import FlightData
import UserInput

"""
Le client veut connaitre a chaque etape:
- position du drone x,z,theta
- position du drone par rapport a la piste (Sera calculé après coup)
- position des gouvernes, et de la commande de gaz
- (Watt.h utilisés)
- rapport de collision avec le sol (force, et quels sont les points qui touchent le sol)
"""
class Logger:
    #Ceci est une variable statique
    file = None

    @staticmethod
    def setup(fileName):
        if fileName[-4:] != ".csv":
            fileName = fileName + ".csv"

        pathToFile = path.relpath(os.getcwd())
        pathToFile = path.join(pathToFile,"logs")
        if not path.exists(pathToFile):
            os.mkdir(pathToFile)
        pathToFile = path.join(pathToFile,fileName)
        Logger.file = open(pathToFile, mode="w")

        Logger.file.write("posAvionX, posAvionZ, assietteAvion, vAvionX, vAvionZ, elevG, elevD, flapsG, flapsD, throttle, col1PosX, col1PosZ, col1ForceX, col1ForceZ, col2PosX, col2PosZ, col2ForceX, col2ForceZ\n")

    @staticmethod
    def pushNewLine(flightData, rawInput, rapportDeCollision):
        assert (Logger.file != None), "Il faut d'abord setup le logger"
        line = ""

        line += str(flightData.getPosAvion().getX())
        line += ","

        line += str(flightData.getPosAvion().getZ())
        line += ","

        line += str(flightData.getAssiette())
        line += ","

        line += str(flightData.getVAvion().getX())
        line += ","

        line += str(flightData.getVAvion().getZ())
        line += ","

        line += str(rawInput.getElevG())
        line += ","

        line += str(rawInput.getElevD())
        line += ","

        line += str(rawInput.getFlapsG())
        line += ","

        line += str(rawInput.getFlapsD())
        line += ","

        line += str(rawInput.getThrottle())
        line += ","

        line += str(rapportDeCollision.getPos1().getX())
        line += ","

        line += str(rapportDeCollision.getPos1().getZ())
        line += ","

        line += str(rapportDeCollision.getForce1().getX())
        line += ","

        line += str(rapportDeCollision.getForce1().getZ())
        line += ","

        line += str(rapportDeCollision.getPos2().getX())
        line += ","

        line += str(rapportDeCollision.getPos2().getZ())
        line += ","

        line += str(rapportDeCollision.getForce2().getX())
        line += ","

        line += str(rapportDeCollision.getForce2().getZ())

        Logger.file.write(line+"\n")





#TESTS
if __name__=="__main__":
    Logger.setup("premierTest")

