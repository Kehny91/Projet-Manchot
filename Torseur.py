import Espace as E

""" Classe Torseur
    permet de definir un torseur
    attribite E.Vecteur : point + ref, definit le point et le referentiel ou on exprime notre torseur  
    attribute E.Vecteur : resultante, resultante du torseur
    attribute float : moment, moment du torseur (en 2D il ne s'agit que d'un float mais en 3D c'est un vecteur)
"""
## attention il faut que les referentiels soient les meme (vecteur, resultante,moment)
class Torseur:
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
 
    """seter/geter

    """   
    def getVecteur(self):
        return self.vecteur

    def setVecteur(self, nexVecteur):
        self.vecteur = nexVecteur
    
    def getResultante(self):
        return self.resultante
    
    def setResultante(self,newResultante):
        self.resultante = newResultante
    
    def getMoment(self):
        return self.moment

    def setMoment(self, newMoment):
        self.moment = newMoment

    """__str__
        utile a l affichage
    """
    def __str__(self):
        return ("Le torseur s'esprime dans le referentiel : " + str(self.vecteur.ref.nom) +
        " au point : " + '('+str(self.vecteur.x) +','+str(self.vecteur.z) + ')' +
        "\nles composantes de la resultante sont les suivantes : " + '('+str(self.resultante.x) +','+str(self.resultante.z) + ')'+
        "\nles composantes du moment sont les suivantes : " + str(self.moment))
        
    """__eq__
        permet la comparaison de deux torseurs (==)
    """
    def __eq__(self,torseur):
        return(self.vecteur == torseur.vecteur and self.resultante == torseur.resultante and self.moment == torseur.moment)
             

        
    """changeRef
        permet de changer le referentiel dans lequel le torseur est exprimé
        @param Refenciel : ref
    """
    def changeRef(self,ref):
        if self.vecteur.ref==ref:
            return self
        else:
            return Torseur(self.vecteur.changeRef(ref),self.resultante.projectionRef(ref),self.moment) #En 2D, le changement de repere n'affecte pas le moment
  
    """changePoint
       Se place dans un referentiel commun (en l'occurance self.ref) et change le point d application du torseur
       @param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
    """        
    def changePoint(self,vecteur):
        if self.vecteur.ref == vecteur.ref:
            Mpoint = self.moment + self.vecteur.pointToVect(vecteur).prodVect(self.resultante)
            return Torseur(vecteur,self.resultante,Mpoint)
        else:
            return self.changeRef(vecteur.ref).changePoint(vecteur)
 
    """__add__
        adition de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
        @param Torseur : torseur, l element a ajouter
    """    
    def __add__(self,torseur):
            if (self.vecteur == torseur.vecteur):
                return Torseur(self.vecteur,self.resultante+torseur.resultante,self.moment+torseur.moment)
            else :
                return self + torseur.changePoint(self.vecteur)
 
    """__sub__
        soustraction de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
        @param Torseur : torseur, l element a soustraire
    """    
    def __sub__(self,torseur):
        if (self.vecteur == torseur.vecteur):
            return Torseur(self.vecteur,self.resultante-torseur.resultante,self.moment-torseur.moment)
        else :
            return self - torseur.changePoint(self.vecteur)
    
    """__pow__
        mutiplication par un scalaire
        @param float : scal, le mutiplicateur
    """
    def __mul__(self,scal):
        return Torseur(self.vecteur,self.resultante*scal, self.moment*scal)
