import numpy as np

class ExceptionNotSameRef(Exception):
    pass

"""Operateur modulo
   @param float : x dividende
   @param float : modulo diviseur
"""
def moduloF(x, modulo):
    if x>=0:
        return x - (x//modulo)*modulo
    else:
        return x - (x//modulo+1)*modulo
        

"""renvoie un angle quelconque dans l'intervalle -pi pi
    @param float : angle en radian
    @throws AngleException : l'angle n'existe pas
"""   
def normalise(angle):
    """ angle = moduloF(angle, 2*np.pi) """
    angle = moduloF(angle,2*np.pi)
    if -np.pi<angle and angle<=np.pi:
        return angle
    elif angle<=-np.pi:
        return normalise(angle + 2*np.pi)
    elif angle>np.pi:
        return normalise(angle - 2*np.pi)
    else:
        assert False,"angle not real: " + str(angle)


"""classe Referentiel et ses methodes
    attribute String : nom, nom du referentiel
    attribute float : angleAxeY, angle par rapport a l'horizontale
    attribute Vecteur : origine, point par rapport au refAbsolue
"""
class Referentiel:
    
    def __init__(self, nom, angleAxeY, origine):
        self.nom=nom
        self.angleAxeY= angleAxeY
        self.origine = origine
    
    def getNom(self):
        return self.nom
        
    def setNom(self, newNom):
        self.nom=newNom
        
    def getAngleAxeY(self):
        return self.angleAxeY
    
    def setAngleAxeY(self, newAngleAxeY):
        self.angleAxeY = newAngleAxeY
        
    def getOrigine(self):
        return self.origine
    
    def setOrigine(self,newOrigine):
        self.origine = newOrigine

    def getAxeX(self):
        return Vecteur(1,0,self)

    def getAxeZ(self):
        return Vecteur(0,1,self)
        
    def __eq__(self, ref):
        if (type(ref)!=type(self)):
            return False
        if (self.nom == ref.nom and self.angleAxeY == ref.angleAxeY):
            return True
        else:
            return False
            
    def __str__(self):
        return "ref " + str(self.nom) + " origine: " + str(self.origine) + " angleRef : " + str(self.angleAxeY)

"""classe ReferentielAbsolu
    creation d'un referentiel sur lequel tout les autres referentiel vont etre places
    herite de la classe Referentiel
"""       
class ReferentielAbsolu(Referentiel):
    def __init__(self):
        super().__init__(nom="refAbs",angleAxeY=0, origine= Vecteur(x=0,z=0,ref=self))
        
""" classe Vecteur et ses methodes
    attribute float : x, composante x
    attribute float : z, composante z
    attribute Referentiel : ref, referentiel utilisé
"""     
class Vecteur:
    
    def __init__(self,x=0,z=0,ref=None):
        self.x=x
        self.z=z
        if (ref==None):
            self.ref = ReferentielAbsolu()
        else:
            self.ref = ref

    def getX(self):
        return self.x

    def getZ(self):
        return self.z

    def getRef(self):
        return self.ref

    def withZmin(self,zMin):
        return Vecteur(self.x,max(zMin,self.z),self.ref)
    
    def __str__(self):
        return "(" + str(self.x) +"," + str(self.z) + ")\\" + str(self.ref.nom)
    
    def __eq__(self,vecteur):
        if (type(vecteur)!=type(self)):
            return False
        return(self.ref==vecteur.ref and self.x == vecteur.x and self.z == vecteur.z)

    def rotate(self,angle):
        angle = normalise(angle)
        return Vecteur(self.x*np.cos(angle)+self.z*np.sin(angle) , self.z*np.cos(angle) - self.x*np.sin(angle),self.ref)
    
    def projectionRef(self,ref): 
        angleRefY = normalise(self.ref.angleAxeY-ref.angleAxeY)
        rotated = self.rotate(angleRefY)
        return Vecteur(rotated.x,rotated.z,ref)

    
    def _translationRef(self,ref):
        """Renvoie le vecteur entre les deux origine Oref->Oself dans les coordonnee de ref"""
        return Vecteur(self.ref.origine.x-ref.origine.x,self.ref.origine.z-ref.origine.z).projectionRef(ref)                       
                      
    def changeRef(self,ref):
        return self._translationRef(ref)+self.projectionRef(ref)
        
    def __add__(self, vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            print(self.ref)
            print(" + ")
            print(vecteur.ref)
            raise ExceptionNotSameRef()
            
    def __sub__(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x-vecteur.x, self.z-vecteur.z, self.ref)
        else : 
            print(self.ref)
            print(" - ")
            print(vecteur.ref)
            raise ExceptionNotSameRef()

    
    def __mul__(self,scal):
        return Vecteur(self.x * scal, self.z * scal, self.ref)
        
    def prodScal(self,vecteur):
        if self.ref == vecteur.ref :
            return self.x*vecteur.x + self.z*vecteur.z
        else:
           raise ExceptionNotSameRef()
            
    def prodVect(self, vecteur):
        if (type(vecteur)!=type(self)): #C'est un scalaire. Dans ce cas, on dit que c'est un vecteur porté par Y
            y = vecteur
            return Vecteur(-1*self.z*y, self.x*y, self.ref)
        if self.ref == vecteur.ref:
            return self.z*vecteur.x - self.x*vecteur.z
        else:
            raise ExceptionNotSameRef()
    
    def norm(self):
        return np.sqrt(self.x**2+self.z**2)
        
    def unitaire(self):
        if self.x==0 and self.z==0:
            return Vecteur(1,0,self.ref)
        else :
            n= self.norm()
            return self*(1/n)

    #Il faut utiliser atan2 pour eviter les divisions par 0
    #Et rajouter un moins pour le sens trigo
    def arg(self):
        """ Renvoie l'angle du vecteur dans son referentiel"""
        return -1*np.arctan2(self.z,self.x)


if __name__ == "__main__":
    from math import pi
    refSol = Referentiel("refSol",0,Vecteur(0,0))
    refAvion = Referentiel("refAvion",pi/2,Vecteur(10,5,refSol))
    refAbs = ReferentielAbsolu()

    print(refSol)
    print(refAvion)

    vecteur1 = Vecteur(2,1,refAvion)
    print("(2,1) ?")
    print("vecteur1 ", vecteur1)
    print("(11,3) ?")
    print("vecteur1refSol", vecteur1.changeRef(refSol))
    print("")
    print("On bouge le refAvion de 1 sur la droite")
    refAvion.setOrigine(refAvion.getOrigine()+Vecteur(1,0,refSol))
    print("(11,5) ?")
    print(refAvion)
    print("(2,1) ?")
    print("vecteur1 ", vecteur1)
    print("(12,3) ?")
    print("vecteur1refSol", vecteur1.changeRef(refSol))
    print("")
    print("On retourne le refAvion")
    refAvion.setAngleAxeY(refAvion.getAngleAxeY()+pi)
    print("(2,1) ?")
    print("vecteur1 ", vecteur1)
    print("(10,7) ?")
    print("vecteur1refSol", vecteur1.changeRef(refSol))

    try:
        vecteur1 + Vecteur(1,0)
    except:
        print("Parfait, ça crash")
