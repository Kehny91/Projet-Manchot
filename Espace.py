# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 18:41:05 2020

@author: tomju
"""
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
    angle = moduloF(angle, 2*np.pi)
    if -np.pi<angle and angle<=np.pi:
        return angle
    elif angle<=-np.pi:
        return normalise(angle + 2*np.pi)
    elif angle>np.pi:
        return normalise(angle - 2*np.pi)
    else:
        assert False,"angle not real: " + str(angle)

# En réalité on utilise juste la classe Point pour definir l'origine des reperes, ensuite on utilise les vecteurs
# il faudrait trouver une solution plus propre...
#l'ideal serait d'avoir un vecteur comme ça on peut utiliser les methodes mais comment init les classes?
"""classe point et ses methodes
    attriute float : x, coordonnee x
    attriute float : z, coordonnee z
"""
class Point:
    
    def __init__(self,x=0,z=0):
        self.x=x
        self.z=z
         
    def __str__(self):
        return("les coordonnees du point sont :"+'('+ str(self.x)+','+str(self.z)+')')
        

"""classe Referentiel et ses methodes
    attribute String : nom, nom du referentiel
    attribute float : angleAxeY, angle par rapport a l'horizontale
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
        if (self.nom == ref.nom and self.angleAxeY == ref.angleAxeY):
            return True
        else:
            return False
            
    def __str__(self):
        return "le referenciel a pour nom : " + str(self.nom) + ", pour origine : " + str(self.origine)  + " et pour angle par rapport à l'horizontale : " + str(self.angleAxeY)
       
""" classe Vecteur et ses methodes
    attribute float : x, composante x
    attribute float : z, composante z
    attribute Referentiel : ref, referentiel utilisé
"""     
class Vecteur:
    
    def __init__(self,x=0,z=0,ref=0):
        self.x=x
        self.z=z
        self.ref = ref
    
    def __str__(self):
        return "Dans le ref : " + str(self.ref.nom) + " les coordonnees sont (" + str(self.x) +"," + str(self.z) + ")"
    
    def __eq__(self,vecteur):
         return(self.ref==vecteur.ref and self.x == vecteur.x and self.z == vecteur.z)
        
    def projectionRef(self,ref): 
        angleRefY = normalise(ref.angleAxeY-self.ref.angleAxeY)
        matriceRot = np.array([[np.cos(angleRefY),-np.sin(angleRefY)],
                               [np.sin(angleRefY), np.cos(angleRefY)]])
        compoOldRef = np.array([[self.x],
                               [self.z]])
        compoNewRef = np.dot(matriceRot,compoOldRef)
        return Vecteur(compoNewRef[0][0],compoNewRef[1][0],ref)
    
    def translationRef(self,ref):
        return Vecteur(ref.origine.x-self.ref.origine.x,ref.origine.z-self.ref.origine.z,Referentiel(0,0,0)).projectionRef(ref)                       
     
#    def HomothetieRef(self,scal):
#        matricePassage = np.array([[scal,      0       ],
#                                   [     0       , scal]])                                  
#        compoOldRef = np.array([[self.x],
#                                [self.z]])
#        compoNewRef = np.dot(matriceTranspo,compoOldRef) 
#        return Vecteur(compoNewRef[0][0],compoNewRef[1][0],ref) 
                      
    def changeRef(self,ref):
        return self.translationRef(ref)+self.projectionRef(ref)
        
    def __add__(self, vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.__add__(vecteur.projectionRef(self.ref))
            
    def __sub__(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x-vecteur.x, self.z-vecteur.z, self.ref)
        else : 
            return self.__sub__(vecteur.projectionRef(self.ref))
            
    def __mul__(self,scal):
        return Vecteur(self.x * scal, self.z * scal, self.ref)
            
    def prodScal(self, vecteur):
        if self.ref == vecteur.ref:
            return self.x*vecteur.z - self.z*vecteur.x
        else:
            return self.prodScal(vecteur.projectionRef(self.ref))
    
    def norm(self):
        return np.sqrt(self.x**2+self.z**2)
    
    def afficheNorm(self,ref):
        if self.ref==ref:
            print "Dans le ref : " + str(self.ref.nom) + "la norme est : " + str(self.norm())
        else:
            return self.projectionRef(ref).afficheNorm(ref)
        
    def unitaire(self):
        if self.x==0 and self.z==0:
            return Vecteur(1,0,self.ref)
        else :
            n= self.norm()
            return Vecteur(self.x/n,self.z/n,self.ref)
