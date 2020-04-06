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

"""classe point et ses methodes
    attriute float : x, coordonnee x
    attriute float : z, coordonnee z
"""
class Point:
    
    def __init__(self,x,z):
        self.x=x
        self.z=z
        
    def distance(self,pointB):
        return ((self.x-pointB.x)**2+(self.z-pointB.z)**2)**0.5
        
    def __str__(self):
        return("les coordonnees du point sont :"+'('+ str(self.x)+','+str(self.z)+')')
        
"""classe Referentiel et ses methodes
    attribute String : nom, nom du referentiel
    attribute float : angleAxeY, angle par rapport a l'horizontale
"""
class Referentiel:
    
    def __init__(self,nom,angleAxeY, origine):
        self.nom=nom
        self.angleAxeY= angleAxeY
        self.origine = Point(0,0)
    
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
    def __init__(self,x,z,ref):
        self.x=x
        self.z=z
        self.ref = ref
        
    def changeRef(self,ref):
        angleRefY = normalise(self.ref.angleAxeY-ref.angleAxeY)
        x = np.cos(angleRefY)*self.x - np.sin(angleRefY)*self.z
        z = np.cos(angleRefY)*self.z + np.sin(angleRefY)*self.x
        return Vecteur(x,z,ref)
        
    def __add__(self, vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.__add__(vecteur.changeRef(self.ref))
            
    def __sub__(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x-vecteur.x, self.z-vecteur.z, self.ref)
        else : 
            return self.__sub__(vecteur.changeRef(self.ref))
            
    def prodScal(self, vecteur):
        if self.ref == vecteur.ref:
            return self.x*vecteur.z - self.z*vecteur.x
        else:
            return self.prodScal(vecteur.changeRef(self.ref))
    
    def norm(self):
        return np.sqrt(self.x**2+self.z**2)
        
    def unitaire(self):
        if self.x==0 and self.y==0:
            return Vecteur(1,0)
        else :
            n= self.norm()
            return Vecteur(self.x/n,self.z/n)
            
    def __str__(self):
        return "Dans le ref : " + str(self.ref.nom) + " les coordonnees sont (" + str(self.x) +"," + str(self.z) + ")"
    
    def afficheNorm(self,ref):
        if self.ref==ref:
            print "Dans le ref : " + str(self.ref.nom) + "la norme est : " + str(self.norm())
        else:
            return self.changeRef(ref).afficheNorm(ref)
