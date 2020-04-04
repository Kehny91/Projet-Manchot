class OutOfBoundException(Exception):
    pass

def checkBoundaries(x, xMin, xMax):
    if (x<xMin or x>xMax):
        raise OutOfBoundException()

def constrain(x, xMin, xMax):
    return min(xMax,max(xMin,x))