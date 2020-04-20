import Espace as E
from copy import copy


## attention il faut que les referentiels soient les meme (vecteur, resultante,moment)
class Torseur:
    """Permet de definir un torseur
    \nattribite E.Vecteur : pointAppl, (point + ref) definit le point et le referentiel ou on exprime notre torseur  
    \nattribute E.Vecteur : resultante, resultante du torseur exprimee dans le même ref que le vecteur
    \nattribute float : moment, moment du torseur
    """
    #Init
    def __init__(self, pointAppl, resultante, moment):
        self.pointAppl = pointAppl
        self.resultante = resultante
        self.moment = moment
    
    #Geter/Seter
    def getPointAppl(self):
        """ Renvoie une copy du vecteur position du torseur"""
        return copy(self.pointAppl)

    def setPointAppl(self, nexPointAppl):
        self.pointAppl = nexPointAppl
    
    def getResultante(self):
        """ Renvoie une copy du vecteur resultante du torseur"""
        return copy(self.resultante)
    
    def setResultante(self,newResultante):
        self.resultante = newResultante
    
    def getMoment(self):
        return copy(self.moment)

    def setMoment(self, newMoment):
        self.moment = newMoment

    #Methodes
    def __str__(self):
        """Utile a l affichage d un Torseur
            \nreturn String
        """
        return ("Le torseur s'exprime dans le referentiel : " + str(self.pointAppl.ref.nom) +
        " au point : " + '('+str(self.pointAppl.x) +','+str(self.pointAppl.z) + ')' +
        "\nles composantes de la resultante sont les suivantes : " + str(self.resultante) +
        "\nles composantes du moment sont les suivantes : " + str(self.moment))
        
    def __eq__(self,torseur):
        """Test si deux torseurs sont identiques
            \nreturn bool
        """ 
        return(self.pointAppl == torseur.pointAppl and self.resultante == torseur.resultante and self.moment == torseur.moment)      

class TorseurEffort(Torseur):
    """Permet de definir un torseur statique
    \nattribite E.Vecteur : pointAppl, (point + ref) definit le point et le referentiel ou on exprime notre torseur  
    \nattribute E.Vecteur : force, resultante du torseur exprimee dans le même ref que le vecteur
    \nattribute float : moment, moment du torseur
    """
    #Init, on s'assure que le vecteur force s'exprime bien dans le ref du vecteur position
    def __init__(self,pointAppl,force = E.Vecteur(0,0),moment=0):
        if pointAppl.ref == force.ref:
            super().__init__(pointAppl,force,moment)
        else:
            super().__init__(pointAppl,force.projectionRef(pointAppl.ref),moment)
    
    #Geter/Seter
    def getForce(self):
        return self.resultante
    
    def setForce(self, newForce):
        self.setResultante(newForce.projectionRef(self.pointAppl.getRef()))

    #Methodes
    def changeRef(self,ref):
        """permet de renvoyer un nouveau torseur ou le referentiel dans lequel le torseur est exprime a ete change
            \n@param Referentiel : ref, le referentiel ou on souhaite exprimer la resultante
            \nreturn Torseur
        """
        if self.pointAppl.ref==ref:
            return self
        else:
            return TorseurEffort(self.pointAppl.changeRef(ref),self.resultante.projectionRef(ref),self.moment)
         
    def changePoint(self,vecteur):
        """Se place dans un referentiel commun (en l'occurance self.ref) et renvoie un torseur ou le point d application du torseur a ete chang
            \n@param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
            \nreturn Torseur
        """ 
        if self.pointAppl.ref == vecteur.ref:
            BA = vecteur.pointToVect(self.pointAppl)
            Mpoint = self.moment + BA.prodVect(self.resultante)
            return TorseurEffort(copy(vecteur),copy(self.resultante),Mpoint)
        else:
            return self.changeRef(vecteur.ref).changePoint(vecteur)
    
    def __add__(self,torseur):
        """Additionne de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
            \n@param Torseur : torseur, l element a ajouter
            \nreturn Torseur
        """ 
        if (self.pointAppl == torseur.pointAppl):
            return TorseurEffort(copy(self.pointAppl),self.resultante+torseur.resultante,self.moment+torseur.moment)
        else :
            return self + torseur.changePoint(self.pointAppl)
    
    def __sub__(self,torseur):        
        """Soustrait deux torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
            \n@param Torseur : torseur, l element a soustraire
            \nreturn Torseur
        """
        if (self.pointAppl == torseur.pointAppl):
            return TorseurEffort(copy(self.pointAppl),self.resultante-torseur.resultante,self.moment-torseur.moment)
        else :
            return self - torseur.changePoint(self.pointAppl)
    
    def __mul__(self,scal):
        """mutiplication du torseur par un scalaire
        \n@param float : scal, le mutiplicateur
        \nreturn Torseur
        """
        return TorseurEffort(copy(self.pointAppl),self.resultante*scal, self.moment*scal) 

class TorseurCinematique(Torseur):
    """Permet de definir un torseur cinematique
    \nattribite E.Vecteur : pointAppl, (point + ref) definit le point et le referentiel ou on exprime notre torseur  
    \nattribute  float : vitesseRotation, resultante du torseur exprimee dans le même ref que le vecteur
    \nattribute E.Vecteur : vitesse, moment du torseur
    """
    #Init
    def __init__(self,pointAppl, VitesseRotation = 0, vitesse = E.Vecteur(0,0)):
        if pointAppl.ref == vitesse.ref:
            super().__init__(pointAppl,VitesseRotation,vitesse)
        else:
            super().__init__(pointAppl,VitesseRotation,vitesse.projectionRef(pointAppl.ref))

    
    #Geter/Seter
    def getW(self):
        return self.getResultante()
    
    def setW(self, w):
        self.setResultante(w)

    def getVitesse(self):
        return self.getMoment()

    def setVitesse(self, v):
        self.setMoment(v.projectionRef(self.pointAppl.getRef()))

    def changeRef(self,ref):
        """permet de renvoyer un nouveau torseur ou le referentiel dans lequel le torseur est exprime a ete change
            \n@param Referentiel : ref, le referentiel ou on souhaite exprimer la resultante
            \nreturn Torseur
        """
        if self.pointAppl.ref==ref:
            return self
        else:
            return TorseurCinematique(copy(self.pointAppl.changeRef(ref)),self.resultante,copy(self.moment.projectionRef(ref)))
         
    def changePoint(self,vecteur):
        """Se place dans un referentiel commun (en l'occurance self.ref) et renvoie un torseur ou le point d application du torseur a ete chang
            \n@param Vecteur : vecteur, le point ou on souhaite exprimer le torseur
            \nreturn Torseur
        """ 
        if self.pointAppl.ref == vecteur.ref:
            BA = vecteur.pointToVect(self.pointAppl)
            BA_ProdVect_Result = E.Vecteur(-BA.z*self.resultante,BA.x*self.resultante,self.pointAppl.ref)
            Va = self.moment + BA_ProdVect_Result
            return TorseurCinematique(copy(vecteur),self.resultante,Va)
        else:
            return self.changeRef(vecteur.ref).changePoint(vecteur)
    
    def __add__(self,torseur):
        """Additionne de torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
            \n@param Torseur : torseur, l element a ajouter
            \nreturn Torseur
        """ 
        if (self.pointAppl == torseur.pointAppl):
            return TorseurCinematique(copy(self.pointAppl),self.resultante+torseur.resultante,self.moment+torseur.moment)
        else :
            return self + torseur.changePoint(self.pointAppl)
    
    def __sub__(self,torseur):        
        """Soustrait deux torseurs, pour cela il faut que les torseurs soient exprimes au meme point, meme referentiel
            \n@param Torseur : torseur, l element a soustraire
            \nreturn Torseur
        """
        if (self.pointAppl == torseur.pointAppl):
            return TorseurCinematique(copy(self.pointAppl),self.resultante-torseur.resultante,self.moment-torseur.moment)
        else :
            return self - torseur.changePoint(self.pointAppl)

    def __mul__(self,scal):
        """mutiplication du torseur par un scalaire
        \n@param float : scal, le mutiplicateur
        \nreturn Torseur
        """
        return TorseurCinematique(copy(self.pointAppl),self.resultante*scal, self.moment*scal) 
         
if __name__ == "__main__":
    from math import pi

    refSol = E.Referentiel("refSol",0,E.Vecteur(0,0))
    refAvion = E.Referentiel("refAvion",pi/2,E.Vecteur(10,5,refSol))
    refAbs = E.ReferentielAbsolu()

    torseurCin = TorseurCinematique(E.Vecteur(0,0,refAvion), 1, E.Vecteur(2,1,refAbs))
    print("v (2,1)\\refAbs ?")
    print(torseurCin.changeRef(refAbs))
    print("")
    print("v (1,1)\\refAbs ?")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion).changeRef(refAbs)))
    print("")
    print("On bouge le ref avion de 1 vers le haut")
    refAvion.setOrigine(refAvion.getOrigine()+E.Vecteur(0,1,refSol))
    print(refAvion)
    print("v (2,1)\\refAbs ?")
    print(torseurCin.changeRef(refAbs))
    print("")
    print("v (1,1)\\refAbs ?")
    print(torseurCin.changePoint(E.Vecteur(1,0,refAvion)).changeRef(refAbs))
    print("")

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

    torseurAction = TorseurEffort(E.Vecteur(0,0,refAvion), E.Vecteur(2,1,refAbs), -1)
    print("v (2,1)\\refAbs ?")
    print("m -1?")
    print(torseurAction.changeRef(refAbs))
    print("")
    print("v (-1,2)\\refAvion ?")
    print("m +1?")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)))
    print("")
    print("On bouge le ref avion de 1 vers le haut")
    refAvion.setOrigine(refAvion.getOrigine()+E.Vecteur(0,1,refSol))
    print(refAvion)
    print("f (2,1)\\refAion ?")
    print("m -1 ?")
    print(torseurAction.changeRef(refAbs))
    print("")
    print("f (2,1)\\refAbs ?")
    print("m +1?")
    print(torseurAction.changePoint(E.Vecteur(1,0,refAvion)).changeRef(refAbs))
    
    refAvion = E.Referentiel("refAvion",pi/2,E.Vecteur(10,5,refSol))
    print("La meme chose mais la force  est donne par rapport au ref avion")
    torseurAction = TorseurEffort(E.Vecteur(0,0,refAvion), E.Vecteur(2,1,refAvion), -1)
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