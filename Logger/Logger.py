import os.path as path
import os
import Data.DataTypes
import time

def formatFloat(x):
    return '{:06.2f}'.format(x)

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
    tStart = 0

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

        Logger.file.write("  time ,  posX  , posZ   ,assiette,   vX   ,   vZ   ,  vRot  ,  elevG ,  elevD , flapsG , flapsD ,throttle,col1PosX,col1PosZ, col1FX , col1FZ ,col2PosX,col2PosZ, col2FX , col2FZ\n")
        Logger.tStart = time.time()

    @staticmethod
    def pushNewLine(flightData, rawInput, rapportDeCollision):
        assert (Logger.file != None), "Il faut d'abord setup le logger"
        line = formatFloat(flightData.getTime())
        line += " , "

        line += formatFloat(flightData.getPosAvion().getX())
        line += " , "

        line += formatFloat(flightData.getPosAvion().getZ())
        line += " , "

        line += formatFloat(flightData.getAssiette())
        line += " , "

        line += formatFloat(flightData.getVAvion().getX())
        line += " , "

        line += formatFloat(flightData.getVAvion().getZ())
        line += " , "

        line += formatFloat(flightData.getW())
        line += " , "

        line += formatFloat(rawInput.getElevG())
        line += " , "

        line += formatFloat(rawInput.getElevD())
        line += " , "

        line += formatFloat(rawInput.getFlapsG())
        line += " , "

        line += formatFloat(rawInput.getFlapsD())
        line += " , "

        line += formatFloat(rawInput.getThrottle())
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getPos1()!=None):
            toAdd = formatFloat(rapportDeCollision.getPos1().getX())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getPos1()!=None):
            toAdd = formatFloat(rapportDeCollision.getPos1().getZ())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getForce1()!=None):
            toAdd = formatFloat(rapportDeCollision.getForce1().getX())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getForce1()!=None):
            toAdd = formatFloat(rapportDeCollision.getForce1().getZ())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getPos2()!=None):
            toAdd = formatFloat(rapportDeCollision.getPos2().getX())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getPos2()!=None):
            toAdd = formatFloat(rapportDeCollision.getPos2().getZ())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getForce2()!=None):
            toAdd = formatFloat(rapportDeCollision.getForce2().getX())
        line += toAdd
        line += " , "

        toAdd = " NONE "
        if (rapportDeCollision.getForce2()!=None):
            toAdd = formatFloat(rapportDeCollision.getForce2().getZ())
        line += toAdd

        Logger.file.write(line+"\n")

    @staticmethod
    def stop():
        if (Logger.file != None):
            Logger.file.close()





#TESTS
if __name__=="__main__":
    Logger.setup("premierTest")

