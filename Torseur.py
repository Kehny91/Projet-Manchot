import Espace as E
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
    
    def __init__(self,vecteur=E.Vecteur(0,0),resultante=E.Vecteur(0,0),moment=0):
        self.vecteur = vecteur
        self.resultante = resultante
        self.moment = moment
    
    #pseudo-surchage, permet de definir directement un torseur (evite de definir deux fois le ref)
    def init2(self,pointx,pointz,ref,resultantex,resultantez,momenty):
        self.vecteur = E.Vecteur(pointx,pointz,ref)
        self.resultante = E.Vecteur(resultantex,resultantez,ref)
        self.moment = momenty
 
    #seter/geter
    def getVecteur(self):
        """ Renvoie une copy du vecteur position du torseur"""
        return copy(self.vecteur)

    def setVecteur(self, nexVecteur):
        self.vecteur = nexVecteur
    
    def getResultante(self):
        """ Renvoie une copy du vecteur resultante du torseur"""
        return copy(self.resultante)
    
    def setResultante(self,newResultante):
        self.resultante = newResultante
    
    def getMoment(self):
        return self.moment

    def setMoment(self, newMoment):
        self.moment = newMoment

   
    def __str__(self):
        """__str__
        utile a l affichage
        """
        return ("Le torseur s'exprime dans le referentiel : " + str(self.vecteur.ref.nom) +
        " au point : " + '('+str(self.vecteur.x) +','+str(self.vecteur.z) + ')' +
        "\nles composantes de la resultante sont les suivantes : " + '('+str(self.resultante.x) +','+str(self.resultante.z) + ') ' +# str(self.resultante.ref)+
        "\nles composantes du moment sont les suivantes : " + str(self.moment))
        
    def __eq__(self,torseur):
        """__eq__
        permet la comparaison de deux torseurs (==)
        """
        return(self.vecteur == torseur.vecteur and self.resultante == torseur.resultante and self.moment == torseur.moment)
             

    def changeRef(self,ref):
        """changeRef
        permet de renvoyer un nouveau torseur où le referentiel dans lequel le torseur est exprimé a été changé
        \n @param E.Refenciel : ref
        """
        if self.vecteur.ref==ref:
            return self
        else:
            return Torseur(self.vecteur.changeRef(ref),self.resultante.projectionRef(ref),self.moment) #En 2D, le changement de repere n'affecte pas le moment
         
    def changePoint(self,vecteur):
        """changePoint
       \n Se place dans un referentiel commun (en l'occurance self.ref) et renvoie un torseur où le point d application du torseur a été changé
       \n @param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
        """ 
        if self.vecteur.ref == vecteur.ref:
            Mpoint = self.moment + vecteur.pointToVect(self.vecteur).prodVect(self.resultante)
            return Torseur(copy(vecteur),copy(self.resultante),Mpoint)
        else:
            return self.changeRef(vecteur.ref).changePoint(vecteur)
    
    def __add__(self,torseur):
    """__add__
        adition de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
        \n @param Torseur : torseur, l element a ajouter
    """ 
            if (self.vecteur == torseur.vecteur):
                return Torseur(copy(self.vecteur),self.resultante+torseur.resultante,self.moment+torseur.moment)
            else :
                return self + torseur.changePoint(self.vecteur)
    
    def __sub__(self,torseur):        
    """__sub__
        soustraction de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
        @param Torseur : torseur, l element a soustraire
    """
        if (self.vecteur == torseur.vecteur):
            return Torseur(copy(self.vecteur),self.resultante-torseur.resultante,self.moment-torseur.moment)
        else :
            return self - torseur.changePoint(self.vecteur)
    
    
    def __mul__(self,scal):
        """__mul__
        mutiplication par un scalaire
        \n @param float : scal, le mutiplicateur
    """
        return Torseur(copy(self.vecteur),self.resultante*scal, self.moment*scal)
