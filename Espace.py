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
"""

class Referentiel:
    
    def __init__(self,nom,angleAxeY):
        self.nom=nom
        self.angleAxeY= angleAxeY
    
    def getNom(self):
        return self.nom
        
    def setNom(self, newNom):
        self.nom=newNom
        
    def getAngleAxeY(self):
        return self.angleAxeY
    
    def setAngleAxeY(self, newAngleAxeY):
        self.angleAxeY = newAngleAxeY
    
    def __affiche__(self):
        print("le referenciel a pour nom : " + str(self.nom) + " et pour angle par rapport à l'horizontale : " + str(self.angleAxeY))

""" classe Vecteur et ses methodes
    attribute float : x, coordonnee x
    attribute float : z, coordonnee z
    attribute Referentiel : ref, referentiel utilisé
"""     
class Vecteur:
    def __init__(self,x,z,ref):
        self.x=x
        self.z=z
        self.ref = ref
        
    def __changeRef__(self,ref):
        angleRefY = normalise(self.ref.angleAxeY-ref.angleAxeY)
        x = np.cos(angleRefY)*self.x - np.sin(angleRefY)*self.z
        z = np.cos(angleRefY)*self.z + np.sin(angleRefY)*self.x
        return Vecteur(x,z,ref)
        
    def __add__(self, vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x+vecteur.x, self.z+vecteur.z, self.ref)
        else : 
            return self.__add__(vecteur.__changeRef__(self.ref))
            
    def __sous__(self,vecteur):
        if self.ref == vecteur.ref:
            return Vecteur(self.x-vecteur.x, self.z-vecteur.z, self.ref)
        else : 
            return self.__sous__(vecteur.__changeRef__(self.ref))
            
    def __prodScal__(self, vecteur):
        if self.ref == vecteur.ref:
            return self.x*vecteur.z - self.z*vecteur.x
        else:
            return self.__prodScal__(vecteur.__changeRef__(self.ref))
    
    def __norm__(self):
        return np.sqrt(self.x**2+self.z**2)
        
    def __unitaire__(self):
        if self.x==0 and self.y==0:
            return Vecteur(1,0)
        else :
            n= self.norm()
            return Vecteur(self.x/n,self.z/n)
            
    def __affiche__(self):
        print("Dans le ref : " + str(self.ref.nom) + " les coordonnees sont (" + str(self.x) +"," + str(self.z) + ")")
    
    def __afficheNorm__(self):
        print("Dans le ref : " + str(self.ref.nom) + "la norme est : " + str(self.__norm__()))
        
    