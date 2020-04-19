import AlexPhy.Espace as E
from copy import copy


## attention il faut que les referentiels soient les meme (vecteur, resultante,moment)
class Torseur:
    """ Classe Torseur
    permet de definir un torseur
    attribite E.Vecteur : point + ref, definit le point et le referentiel ou on exprime notre torseur  
    attribute E.Vecteur : resultante, resultante du torseur exprimee dans le même ref que le vecteur
    attribute float : moment, moment du torseur (en 2D il ne s'agit que d'un float mais en 3D c'est un vecteur)
"""
    #Init
    
    def __init__(self, position, resultante, moment):
        self.position = position
        self.resultante = resultante
        self.moment = moment
 
    #seter/geter
    def getPosition(self):
        """ Renvoie une copy du vecteur position du torseur"""
        return copy(self.position)

    def setPosition(self, position):
        self.position = position
    
    def getResultante(self):
        """ Renvoie une copy du vecteur resultante du torseur"""
        return copy(self.resultante)
    
    def setResultante(self,newResultante):
        self.resultante = newResultante
    
    def getMoment(self):
        return copy(self.moment)

    def setMoment(self, moment):
        self.moment = moment

   
    def __str__(self):
        return "Torseur: pos " + str(self.position) + "\nresultante " + str(self.resultante) + "\nmoment "  + str(self.moment)
        
    def __eq__(self,torseur):
        """__eq__
        permet la comparaison de deux torseurs (==)
        """
        return(self.position == torseur.position and self.resultante == torseur.resultante and self.moment == torseur.moment)
         
    def changePoint(self,vecteur):
        """changePoint
        \n Se place dans un referentiel commun (en l'occurance self.ref) et renvoie un torseur où le point d application du torseur a été changé
        \n @param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
        """ 
        if self.position.ref == vecteur.ref:
            Mpoint = self.moment + (self.position - vecteur).prodVect(self.resultante)
            return Torseur(copy(vecteur),copy(self.resultante),Mpoint)
        else:
            raise E.ExceptionNotSameRef()
    
    def __add__(self,torseur):
        pass #Depend de si l'on est cinematique ou effort
        """__add__
        adition de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
        \n @param Torseur : torseur, l element a ajouter
        
        if (self.position == torseur.position):
            return Torseur(copy(self.position), self.resultante + torseur.resultante.projectionRef(self.resultante.ref) , self.moment+torseur.moment)
        else :
            return self + torseur.changePoint(self.position)
        """
    
    def __sub__(self,torseur):  
        pass #Depend de si l'on est cinematique ou effort      
        """__sub__
        soustraction de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
        @param Torseur : torseur, l element a soustraire
        
        if (self.vecteur == torseur.vecteur):
            return Torseur(copy(self.vecteur),self.resultante-torseur.resultante,self.moment-torseur.moment)
        else :
            return self - torseur.changePoint(self.vecteur)
        """
    
    
    def __mul__(self,scal):
        """__mul__
        mutiplication par un scalaire
        \n @param float : scal, le mutiplicateur
        """
        return Torseur(copy(self.vecteur),self.resultante*scal, self.moment*scal)
