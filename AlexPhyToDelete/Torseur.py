if __name__ != "__main__":
    import AlexPhy.Espace as E
else:
    import Espace as E
from copy import copy


## attention il faut que les referentiels soient les meme (vecteur, resultante,moment)
class _Torseur:
    """ Classe Torseur
    permet de definir un torseur
    attribite E.Vecteur : point + ref, definit le point et le referentiel ou on exprime notre torseur  
    attribute E.Vecteur : resultante, resultante du torseur exprimee dans le même ref que le vecteur
    attribute float : moment, moment du torseur (en 2D il ne s'agit que d'un float mais en 3D c'est un vecteur)
"""
    #Init
    
    def __init__(self, position, resultante, moment):
        self._position = position
        self._resultante = resultante
        self._moment = moment
 
    #seter/geter
    def getPosition(self):
        """ Renvoie une copy du vecteur position du torseur"""
        return copy(self._position)

    def setPosition(self, position):
        self._position = position
    
    def getResultante(self):
        """ Renvoie une copy du vecteur resultante du torseur"""
        return copy(self._resultante)
    
    def setResultante(self,newResultante):
        self._resultante = newResultante
    
    def getMoment(self):
        return copy(self._moment)

    def setMoment(self, moment):
        self._moment = moment

    def changeRef(self, ref):
        self._position = self._position.changeRef(ref)

   
    def __str__(self):
        return "Torseur: pos " + str(self._position) + " resultante " + str(self._resultante) + " moment "  + str(self._moment)
        
    def __eq__(self,torseur):
        """__eq__
        permet la comparaison de deux torseurs (==)
        """
        return(self._position == torseur.getPosition() and self._resultante == torseur.getResultante() and self._moment == torseur.getMoment())


    #Add et Sub depende de si Moment est un vecteur ou non
    
    
    def __mul__(self,scal):
        """__mul__
        mutiplication par un scalaire
        \n @param float : scal, le mutiplicateur
        """
        return self.__class__(copy(self._position),self._resultante*scal, self._moment*scal)

class TorseurAction(_Torseur):
    def __init__(self, position, force, moment):
        super().__init__(position,force,moment)

    def getForce(self):
        return self.getResultante()

    #def getMoment(self):
    #    return self.getMoment()

    def __add__(self, other):
        if (self._position.getRef() != other.getPosition().getRef()):
            raise E.ExceptionNotSameRef()
        if (self._position == other.getPosition()):
            return TorseurAction(copy(self._position), self._resultante + other.getResultante().projectionRef(self._resultante.getRef()) , self._moment + other.getMoment())
        else :
            other = other.changePoint(self._position)
            return self + other

    def __sub__(self, other):
        if (self._position.getRef() != other.getPosition.getRef()):
            raise E.ExceptionNotSameRef()
        if (self._position == other.getPosition()):
            return TorseurAction(copy(self._position), self._resultante - other.getResultante().projectionRef(self._resultante.getRef()) , self._moment - other.getMoment())
        else :
            other = other.changePoint(self._position)
            return self - other

    def changePoint(self,vecteur):
        """changePoint
        \n Se place dans un referentiel commun (en l'occurance self.ref) et renvoie un torseur où le point d application du torseur a été changé
        \n @param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
        """ 
        if self._position.getRef() == vecteur.getRef():
            Mpoint = self._moment + ((self._position - vecteur.changeRef(self._position.getRef())).prodVect(self._resultante.projectionRef(self._position.getRef())))
            return self.__class__(copy(vecteur),copy(self._resultante),Mpoint) #Il ne faut pas utiliser _Torseur sinon on perd notre polymorphisme
        else:
            return self.changePoint(vecteur.changeRef(self._position.getRef()))

class TorseurCinematique(_Torseur):
    def __init__(self, position, w, vitesse):
        super().__init__(position, w, vitesse)

    def getW(self):
        return self.getResultante()

    def getVitesse(self):
        return self.getMoment()

    def setW(self, w):
        self.setResultante(w)

    def setV(self, v):
        self.setMoment(v)

    def __add__(self, other):
        if (self._position == other.getPosition()):
            return TorseurCinematique(copy(self._position), self._resultante + other.getResultante() , self._moment + other.getMoment().projectionRef(self._resultante.getRef()))
        else :
            return self + other.changePoint(self._position)

    def __sub__(self, other):
        if (self._position == other.getPosition()):
            return TorseurCinematique(copy(self._position), self._resultante - other.getResultante() , self._moment - other.getMoment().projectionRef(self._resultante.getRef()))
        else :
            return self - other.changePoint(self._position)

    def changePoint(self,vecteur):
        """changePoint
        \n Se place dans un referentiel commun (en l'occurance self.ref) et renvoie un torseur où le point d application du torseur a été changé
        \n @param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
        """ 
        if self._position.getRef() == vecteur.getRef():
            Mpoint = self._moment + ((self._position - vecteur.changeRef(self._position.getRef())).prodVect(self._resultante)).projectionRef(self._moment.getRef())
            return self.__class__(copy(vecteur),copy(self._resultante),Mpoint) #Il ne faut pas utiliser _Torseur sinon on perd notre polymorphisme
        else:
            return self.changePoint(vecteur.changeRef(self._position.getRef()))

    def applyAction(self, torseurAction, totMass, totInertie, dt):
        torseurAction = torseurAction.changePoint(self.getPosition())
        self._resultante = self._resultante + torseurAction.getMoment()*(dt/totInertie)
        self._moment = self._moment + torseurAction.getForce().projectionRef(self._moment.getRef())*(dt/totMass)

if __name__ == "__main__":
    from math import pi
    refSol = E.Referentiel("refSol",0,E.Vecteur(0,0))
    refAvion = E.Referentiel("refAvion",pi/2,E.Vecteur(10,5,refSol))
    refAbs = E.ReferentielAbsolu()

    torseurCin = TorseurCinematique(E.Vecteur(0,0,refAvion), 1, E.Vecteur(2,1,refAbs))
    print("v (2,1)\\refAbs ?")
    print(torseurCin)
    print("")
    print("v (1,1)\\refAbs ?")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion)))
    print("")
    print("On bouge le ref avion de 1 vers le haut")
    refAvion.setOrigine(refAvion.getOrigine()+E.Vecteur(0,1,refSol))
    print(refAvion)
    print("v (2,1)\\refAbs ?")
    print(torseurCin)
    print("")
    print("v (1,1)\\refAbs ?")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion)))
    print("")
    print("On tourne le ref de pi/2")
    refAvion.setAngleAxeY(refAvion.getAngleAxeY()+pi/2)
    print("v (2,1)\\refAbs ?")
    print(torseurCin)
    print("")
    print("v (2,2)\\refAbs ?")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion)))

    refAvion = E.Referentiel("refAvion",pi/2,E.Vecteur(10,5,refSol))
    print("La meme chose mais la vitesse du ref est donne par rapport au ref avion")
    torseurCin = TorseurCinematique(E.Vecteur(0,0,refAvion), 1, E.Vecteur(2,1,refAvion))
    print("v (2,1)\\refAvion ?")
    print(torseurCin)
    print("")
    print("v (2,0)\\refAvion ?")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion)))
    print("v (0,-2\\refSol)")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion)).getVitesse().projectionRef(refSol))

    print("========= ACTION =============")

    refSol = E.Referentiel("refSol",0,E.Vecteur(0,0))
    refAvion = E.Referentiel("refAvion",pi/2,E.Vecteur(10,5,refSol))
    refAbs = E.ReferentielAbsolu()

    torseurAction = TorseurAction(E.Vecteur(0,0,refAvion), E.Vecteur(2,1,refAbs), -1)
    print("v (2,1)\\refAbs ?")
    print("m -1?")
    print(torseurAction)
    print("")
    print("v (2,1)\\refAbs ?")
    print("m +1?")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)))
    print("")
    print("On bouge le ref avion de 1 vers le haut")
    refAvion.setOrigine(refAvion.getOrigine()+E.Vecteur(0,1,refSol))
    print(refAvion)
    print("f (2,1)\\refAbs ?")
    print("m -1 ?")
    print(torseurAction)
    print("")
    print("f (2,1)\\refAbs ?")
    print("m +1?")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)))
    
    print("")
    print("On tourne le ref de pi/2")
    refAvion.setOrigine(E.Vecteur(10,5,refSol))
    refAvion.setAngleAxeY(refAvion.getAngleAxeY()+pi/2)
    print("f (2,1)\\refAbs ?")
    print("m -1")
    print(torseurAction)
    print("")
    print("f (2,1)\\refAbs ?")
    print("m -2?")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)))
    
    refAvion = E.Referentiel("refAvion",pi/2,E.Vecteur(10,5,refSol))
    print("La meme chose mais la force  est donne par rapport au ref avion")
    torseurAction = TorseurAction(E.Vecteur(0,0,refAvion), E.Vecteur(2,1,refAvion), -1)
    print("f (2,1)\\refAvion ?")
    print("m -1")
    print(torseurAction)
    print("")
    print("f (2,1)\\refAvion ?")
    print("m 0")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)))
    print("")
    print("on tourne de pi/2")
    refAvion.setAngleAxeY(refAvion.getAngleAxeY()+pi/2)
    print("f (2,1)\\refAvion ?")
    print("m -1")
    print(torseurAction)
    print("")
    print("f (2,1)\\refAvion ?")
    print("m 0")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)))

    
