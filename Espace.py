import numpy as np

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
    attribute vecteur : origine, point par rapport au refAbsolue
"""
class Referentiel:
    
    def __init__(self,nom=0,angleAxeY=0, origine=0):
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
        
    def __eq__(self, ref):
        if (type(ref)!=type(self)):
            return False
        if (self.nom == ref.nom and self.angleAxeY == ref.angleAxeY):
            return True
        else:
            return False
            
    def __str__(self):
        return "le referenciel a pour nom : " + str(self.nom) + ", pour origine : " + '(' + str(self.origine.x)  +',' + str(self.origine.z) + ')' +" et pour angle par rapport à l'horizontale : " + str(self.angleAxeY) + " dans le refAbsolu"

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

    def withZmin(self,zMin):
        return Vecteur(self.x,max(zMin,self.z),self.ref)
    
    def __str__(self):
        return "Dans le ref : " + str(self.ref.nom) + " les coordonnees sont (" + str(self.x) +"," + str(self.z) + ")"
    
    def __eq__(self,vecteur):
        if (type(vecteur)!=type(self)):
            return False
        return(self.ref==vecteur.ref and self.x == vecteur.x and self.z == vecteur.z)

    def rotate(self,angle):
        angle = normalise(angle)
        #Pour le 3D, utiliser une matrice de rotation
        #matriceRot = np.array([[np.cos(angle),np.sin(angle)],
        #                       [-np.sin(angle), np.cos(angle)]])
        #compoOldRef = np.array([[self.x],
        #                        [self.z]])
        #compoNewRef = np.dot(matriceRot,compoOldRef)
        #return Vecteur(compoNewRef[0][0],compoNewRef[1][0],self.ref)
        return Vecteur(self.x*np.cos(angle)+self.z*np.sin(angle) , self.z*np.cos(angle) - self.x*np.sin(angle),self.ref)
    
    def projectionRef(self,ref): 
        angleRefY = normalise(ref.angleAxeY-self.ref.angleAxeY)
        rotated = self.rotate(angleRefY)
        return Vecteur(rotated.x,rotated.z,ref)

    """Renvoie le vecteur entre les deux origine Oerf-Oself
    """
    def translationRef(self,ref):
        return Vecteur(self.ref.origine.x-ref.origine.x,self.ref.origine.z-ref.origine.z).projectionRef(ref)                       
                      
    def changeRef(self,ref):
        return self.translationRef(ref)+self.projectionRef(ref)
        
    def __add__(self, vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.__add__(vecteur.projectionRef(self.ref))
    
    def addPoint(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.addPoint(vecteur.changeRef(self.ref))
            
    def __sub__(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x-vecteur.x, self.z-vecteur.z, self.ref)
        else : 
            return self.__sub__(vecteur.projectionRef(self.ref))
    
    def pointToVect(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(vecteur.x-self.x,vecteur.z-self.z, self.ref)
        else : 
            return self.pointToVect(vecteur.changeRef(self.ref))
    
    def __mul__(self,scal):
        return Vecteur(self.x * scal, self.z * scal, self.ref)
        
    def prodScal(self,vecteur):
        if self.ref == vecteur.ref :
            return self.x*vecteur.x + self.z*vecteur.z
        else:
            return self.prodScal(vecteur.projectionRef(self.ref))
            
    def prodVect(self, vecteur):
        if self.ref == vecteur.ref:
            return self.z*vecteur.x - self.x*vecteur.z
        else:
            return self.prodVect(vecteur.projectionRef(self.ref))
    
    def norm(self):
        return np.sqrt(self.x**2+self.z**2)

    def afficheNorm(self,ref):
        if self.ref==ref:
            print ("Dans le ref : " + str(self.ref.nom) + "la norme est : " + str(self.norm()))
        else:
            return self.projectionRef(ref).afficheNorm(ref)
        
    def unitaire(self):
        if self.x==0 and self.z==0:
            return Vecteur(1,0,self.ref)
        else :
            n= self.norm()
            return self*(1/n)
