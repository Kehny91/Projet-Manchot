# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 17:12:00 2020

@author: tomju
"""
import Espace as E
import numpy as np

# Test la methode modulo
print("__methode_modulo__") 
print("3modulo2 : (1?) " +str(E.moduloF(3,2)))    
print("__Fin_Test_methode_modulo__") 
print("\n") 
   
# Test la methode normalise
print("__methode_normalise__")
print("nomrmalise Pi : " + str(E.normalise(1*np.pi))) 
print("nomrmalise 3*Pi : (=Pi?) " + str(E.normalise(3*np.pi))) 
print("nomrmalise 3/2*Pi : (=-1/2*Pi?) " + str(E.normalise(float(1.5*np.pi))))       
print("normalise -1/2*Pi : (=1/2*Pi?) " + str(E.normalise(float(-1.5*np.pi))))
print("__Fin_Test_methode_normalise__") 
print("\n")

# Test de la classe référentiel
print("__classe_Referentiel___")
#constructeur
print("___Init___")   
refTerrestre = E.Referentiel("refTerrestre",10)  
print("Init_Fin")
print("\n")
#geter
print("__Geter__")
print("Nom du referenctiel apres init : " + str(refTerrestre.getNom()))
print("Angle du referenctiel apres init : " + str(refTerrestre.getAngleAxeY()))
refTerrestre.__affiche__()
print("\n")
#seter
print("__seter__")
refTerrestre.setNom("refTerrestre")
refTerrestre.setAngleAxeY(0)
print("Nom du referenctiel apres seter : " + str(refTerrestre.getNom()))
print("Angle du referenctiel apres seter : " + str(refTerrestre.getAngleAxeY()))
print("\n")
print("Fin_Test_Classe_Referentiel")
print("\n")



# Test de la classe vecteur
print("__classe_Vecteur__")
#Constructeur
print("__Init__")
refAero = E.Referentiel("refAero",np.pi/2)

vecteur1 = E.Vecteur(3,4,refTerrestre)

vecteur2 = E.Vecteur(1,6,refAero)

vecteur3 = E.Vecteur(1,6,refTerrestre)

print("Init_Fin")
print("\n")

#methode
print("__methode_")

print("__affiche__")
vecteur1.__affiche__()
vecteur2.__affiche__()
print("__changeRef__")
print("vecteur1 dans le refAero = vecteur(5,-1,refAero)? ")
vecteur1.__changeRef__(refAero).__affiche__()

print("__add__")
print("vecteur1 + vecteur3 = vecteur(2,11,refTerrestre)? ")
vecteur1.__add__(vecteur3).__affiche__()
print("vecteur1 + vecteur2 = vecteur(-5,6,refTerrestre)? ")
vecteur1.__add__(vecteur2).__affiche__()

print("__sous__")
print("vecteur1 + vecteur3 = vecteur(2,-2,refTerrestre)? ")
vecteur1.__sous__(vecteur3).__affiche__()
print("vecteur1 + vecteur2 = vecteur(9,3,refTerrestre)? ")
vecteur1.__sous__(vecteur2).__affiche__()

print("__norm__ + __afficheNorm__")
print("la norme du vecteur1 est egal a 5 : ?")
vecteur1.__afficheNorm__()

print("__prodScal__")
print("le produit scalaire de vecteur1 et vecteur3 = 14?")
print(vecteur1.__prodScal__(vecteur3))
print("le produit scalaire de vecteur2 et vecteur2 = 27?")
print(vecteur1.__prodScal__(vecteur2))
