from math import pi,sin,cos,atan2,sqrt


def moduloF(x, modulo):
    """Operateur modulo
    \n param float : x dividende
    \n param float : modulo diviseur
    """
    if x>=0:
        return x - (x//modulo)*modulo
    else:
        return x - (x//modulo+1)*modulo
         
def normalise(angle):
    """renvoie un angle quelconque dans l'intervalle -pi pi
    \n param float : angle en radian
    \n throws AngleException : l'angle n'existe pas
    """  
    angle = moduloF(angle,2*pi)
    if -pi<angle and angle<=pi:
        return angle
    elif angle<=-pi:
        return normalise(angle + 2*pi)
    elif angle>pi:
        return normalise(angle - 2*pi)
    else:
        assert False,"angle not real: " + str(angle)

class Referentiel:
    """Defini un referentiel
    \n attribute String : nom, nom du referentiel
    \n attribute float : angleAxeY, angle par rapport a l horizontale
    \n attribute Vecteur : origine, point par rapport au refAbsolu
    """
    #Init
    def __init__(self,nom=0,angleAxeY=0, origine=0):
        self.nom=nom
        self.angleAxeY= angleAxeY
        self.origine = origine
    
    #Geter/Seter
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

    #methodes  
    def __eq__(self, ref):
        """Test si deux referentiels sont identiques
        \nreturn bool
        """
        if (type(ref)!=type(self)):
            return False
        if (self.nom == ref.nom and self.angleAxeY == ref.angleAxeY):
            return True
        else:
            return False
    
    def __str__(self):
        """Permet d'afficher un referentiel dans la console
            \nretrun String
        """
        return "Le referenciel a pour nom : " + str(self.nom) + ", pour origine : " + '(' + str(self.origine.x)  +',' + str(self.origine.z) + ')' +" et pour angle par rapport à l'horizontale : " + str(self.angleAxeY) + " dans le refAbsolu"

       
class ReferentielAbsolu(Referentiel):
    """Creation d un referentiel sur lequel tout les autres referentiels vont etre places
    \n Herite de la classe Referentiel
    """
    #Init
    def __init__(self):
        super().__init__(nom="refAbs",angleAxeY=0, origine= Vecteur(x=0,z=0,ref=self))
             
class Vecteur:
    """Defini un Vecteur
    \n attribute float : x, composante x
    \n attribute float : z, composante z
    \n attribute Referentiel : ref, referentiel utilise
    """
    #Init
    def __init__(self,x=0,z=0,ref=None):
        self.x=x
        self.z=z
        if (ref==None):
            self.ref = ReferentielAbsolu()
        else:
            self.ref = ref
    #Geter/Seter
    def getX(self):
        return self.x

    def getZ(self):
        return self.z

    def getRef(self):
        return self.ref

    #methodes
    def withZmin(self,zMin):
        return Vecteur(self.x,max(zMin,self.z),self.ref)
    
    def __str__(self):
        """Utile a l affichage d un vecteur
            \nreturn String
        """
        return "Dans le ref : " + str(self.ref.nom) + " les coordonnees sont (" + str(self.x) +"," + str(self.z) + ")"

    def debug(self):
        """ renvoie un string d'une ligne"""
        return "("+str(self.x) +"," + str(self.z) + ")"+"\\"+str(self.ref.nom)

    def __eq__(self,vecteur):
        """Test si deux vecteurs sont identiques
            \nreturn bool
        """ 
        if (type(vecteur)!=type(self)):
            return False
        return(self.ref==vecteur.ref and self.x == vecteur.x and self.z == vecteur.z)

    def rotate(self,angle):
        """Tourne un vecteur d un angle dans son referentiel
            \nreturn Vecteur
        """
        angle = normalise(angle)
        return Vecteur(self.x*cos(angle)+self.z*sin(angle) , self.z*cos(angle) - self.x*sin(angle),self.ref)
    
    def projectionRef(self,ref):
        """Projete le vecteur dans un autre referentiel
            \nreturn Vecteur
        """ 
        angleRefY = normalise(self.ref.angleAxeY-ref.angleAxeY)
        rotated = self.rotate(angleRefY)
        return Vecteur(rotated.x,rotated.z,ref)

    
    def translationRef(self,ref):
        """Renvoie le vecteur entre les deux origine Oref->Oself dans le ref
            \nreturn Vecteur
        """
        return Vecteur(self.ref.origine.x-ref.origine.x,self.ref.origine.z-ref.origine.z).projectionRef(ref)                       
    

    def changeRef(self,ref):
        """Renvoie un vecteur entre l origine de ref et self
            \nreturn Vecteur
        """
        return self.translationRef(ref)+self.projectionRef(ref)
        
    def __add__(self, vecteur):
        """Somme de deux vecteurs
            \nreturn Vecteur
        """
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.__add__(vecteur.projectionRef(self.ref))
    
    def addPoint(self,vecteur):
        """Somme de deux vecteurs defeni par des point dans self ref
            \nreturn Vecteur
        """
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.addPoint(vecteur.changeRef(self.ref))
            
    def __sub__(self,vecteur):
        """Soustraction de deux vecteurs
            \nreturn Vecteur
        """
        if self.ref == vecteur.ref:
            return Vecteur(self.x-vecteur.x, self.z-vecteur.z, self.ref)
        else : 
            return self.__sub__(vecteur.projectionRef(self.ref))
    
    def pointToVect(self,vecteur):
        """Revoie un vecteur defini pas deux points
            \nreturn Vecteur
        """
        if self.ref == vecteur.ref:
            return Vecteur(vecteur.x-self.x,vecteur.z-self.z, self.ref)
        else : 
            return self.pointToVect(vecteur.changeRef(self.ref))
    
    def __mul__(self,scal):
        """Multiplication par un scalaire
            \nreturn Vecteur
        """
        return Vecteur(self.x * scal, self.z * scal, self.ref)

    def prodScal(self,vecteur):
        """Produit scalaire de deux vecteurs
            \nreturn float
        """
        if self.ref == vecteur.ref :
            return self.x*vecteur.x + self.z*vecteur.z
        else:
            return self.prodScal(vecteur.projectionRef(self.ref))
            
    def prodVect(self, vecteur):
        """Produit vectoriel de deux vecteurs
            \nreturn float
        """
        if self.ref == vecteur.ref:
            return self.z*vecteur.x - self.x*vecteur.z
        else:
            return self.prodVect(vecteur.projectionRef(self.ref))
    
    def norm(self):
        """Renvoie la norme du vecteur
            \nreturn float
        """
        return sqrt(self.x**2+self.z**2)

    def unitaire(self):
        """Renvoie un vecteur unitaire conservant la direction
            \nreturn Vecteur
        """
        if self.x==0 and self.z==0:
            return Vecteur(1,0,self.ref)
        else :
            n= self.norm()
            return self*(1/n)

    def arg(self):
        """ Renvoie l'angle du vecteur dans son referentiel
            \nreturn float
        """
        return -1*atan2(self.z,self.x)

#__________________Test___________________
if __name__ == "__main__":
    ## Test la methode modulo
    print("__methode_modulo__") 
    print("3modulo2 : (1?) " +str(moduloF(3,2)))
    print("3modulo2 : (0.2?) " +str(moduloF(3.5,1.1)))     
    print("__Fin_Test_methode_modulo__") 
    print("\n") 

    # Test la methode normalise
    print("__methode_normalise__")
    print("nomrmalise Pi : " + str(normalise(1*pi))) 
    print("nomrmalise 3*Pi : (=Pi?) " + str(normalise(3*pi))) 
    print("nomrmalise 3/2*Pi : (=-1/2*Pi?) " + str(normalise(float(1.5*pi))))       
    print("normalise -1/2*Pi : (=1/2*Pi?) " + str(normalise(float(-1.5*pi))))
    print("__Fin_Test_methode_normalise__") 
    print("\n")


    # Test de la classe référentiel
    print("__classe_Referentiel___")
    #constructeur
    print("___Init___")   
    refTerrestre = Referentiel("refTerrestre",10,Vecteur(1,1)) 
    refAero = Referentiel("refAero",pi/2,Vecteur(3,5))
    print("Init_Fin")
    print("\n")
    #geter
    print("__Geter__")
    print("Nom du referenctiel apres init : " + str(refTerrestre.getNom()))
    print("Angle du referenctiel apres init : " + str(refTerrestre.getAngleAxeY()))
    print(refTerrestre)
    print("\n")
    #seter
    print("__seter__")
    refTerrestre.setNom("refTerrestre")
    refTerrestre.setAngleAxeY(0)
    refTerrestre.setOrigine(Vecteur(0,0))
    print("Nom du referenctiel apres seter : " + str(refTerrestre.getNom()))
    print("Angle du referenctiel apres seter : " + str(refTerrestre.getAngleAxeY()))
    print("\n")
    #eq
    print("__eq__")
    print("refTerrestre == refAero? " + str(refTerrestre == refAero))
    print("refTerrestre == refTerrestre? " + str(refTerrestre == refTerrestre))
    print("\n")
    #__str__
    print("__str__")
    print(refTerrestre)
    print("\n")
    print("Fin_Test_Classe_Referentiel")
    print("\n")



    # Test de la classe vecteur
    print("__classe_Vecteur__")
    #Constructeur
    print("__Init__")
    vecteur1 = Vecteur(3,4,refTerrestre)
    vecteur2 = Vecteur(1,6,refAero)
    vecteur3 = Vecteur(1,6,refTerrestre)
    print("Init_Fin")
    print("\n")

    #methode
    print("__methode_")

    print("__str__")
    print(vecteur1)
    print(vecteur2)
    print("\n")
    print ("__eq__")
    print("vecteur1==vecteur1 ? "+str(vecteur1==vecteur1))
    print ("vecteur1==vecteur2 ? "+str(vecteur1==vecteur2))
    print ("vecteur1==vecteur3 ? "+str(vecteur1==vecteur3))
    print ("vecteur1 == E.vecteur(3,4,refAero)" + str(vecteur1 == Vecteur(3,4,refAero)))
    print("\n")
    print("__projectionRef__")
    print("projection du vecteur1 dans le refAero = vecteur(-4,3,refAero)? ") #SENS HORAIRE GODAMMIT
    print(vecteur1.projectionRef(refAero))
    print("si on revient dans le refTerrestre = vecteur(3,4)?")
    print(vecteur1.projectionRef(refAero).projectionRef(refTerrestre))
    print("\n")
    print("__translation__")
    print("translation de l'origine du refTerrestre dans le refAero = vecteur(3,5,refAero)? ")
    print(vecteur2.translationRef(refTerrestre))
    print("translation de l'origine du refTerrestre dans le refAero = vecteur(5,-3,refAero)? ") #SENS HORAIRE GODAMMIT
    print(vecteur1.translationRef(refAero))
    print("\n")
    print("__changeRef__")
    print("Le vecteur1 dans le refAero = vecteur(1,0,refAero)? ") #SENS HORAIRE GODAMMIT
    print(vecteur1.changeRef(refAero))
    print("si on revient dans le refTerrestre = vecteur(3,4)?")
    print(vecteur1.changeRef(refAero).changeRef(refTerrestre))
    print("Le vecteur2 dans le refTerrestre = vecteur(9,4,refAero)?")
    print(vecteur2.changeRef(refTerrestre))
    print("\n")
    print("__add__")
    print("vecteur1 + vecteur3 = vecteur(4,10,refTerrestre)? ")
    print(vecteur1+vecteur3)
    print("vecteur1 + vecteur2 = vecteur(-3,5,refTerrestre)? ")
    print(vecteur1+vecteur2)
    print("\n")
    print("__addPoint__")
    print("vecteur1.addPoint(vecteur2) = (0,10)?")
    print(vecteur1.addPoint(vecteur2))
    print("\n")
    print("__sub__")
    print("vecteur1 - vecteur3 = vecteur(2,-2,refTerrestre)? ")
    print(vecteur1-vecteur3)
    print("vecteur1 - vecteur2 = vecteur(9,3,refTerrestre)? ")
    print(vecteur1-vecteur2)
    print("\n")
    print("__pointToVect__")
    print("vecteur1.pointToVect(vecteur2) = vecteur(-6,2,refTerrestre)?")
    print(vecteur1.pointToVect(vecteur2))
    print("\n")
    print("__mul__")
    print("la mutiplication de vecteur1 par une scalaire (3.5) : (10.5,14)?")
    print(vecteur1*3.5)
    print("\n")
    print("__prodScal__")
    print("le produit scalaire de vecteur1 et vecteur2 = ")
    print("\n")
    print("__prodVect__")
    print("le produit vectoriel de vecteur1 et vecteur3 = -14?")
    print(vecteur1.prodVect(vecteur3))
    print("le produit vectoriel de vecteur1 et vecteur2 = -27?")
    print(vecteur1.prodVect(vecteur2))
    print("\n")
    print("__norm__")
    print("la norme du vecteur1 est egal a 5 dans refterrestre: ?")
    print(vecteur1.norm())
    print("\n")
    print("unitaire")
    print("vecteur unitaire de (0,0), (1,0) par def ? :" + str(Vecteur(0,0,refTerrestre).unitaire()))
    print("vecteur unitaire de vecteur1 , (0.6,0.8)? " +str(vecteur1.unitaire()))
    print("\n")
    print("arg")
    print("vecteur1 arg  = -0.927")
    print(vecteur1.arg())