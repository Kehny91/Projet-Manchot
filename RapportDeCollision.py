class RapportDeCollision:
    def __init__(self, pos1 = None, force1 = None, pos2 = None, force2 = None):
        self.pos1 = pos1
        self.force1 = force1
        self.pos2 = pos2
        self.force2 = force2
    
    def addImpact(self, pos, force):
        if (self.pos1 == None and self.force1==None):
            self.pos1 = pos
            self.force1 = force
        elif (self.pos2 == None and self.force2 == None):
            self.pos2 = pos
            self.force2 = force
        else:
            assert False, "Trop d'impactes"

    def getPos1(self):
        return self.pos1

    def getPos2(self):
        return self.pos2

    def getForce1(self):
        return self.force1

    def getForce2(self):
        return self.force2