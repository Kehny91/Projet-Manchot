# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 17:12:00 2020

@author: tomju
"""
import Espace as E
import numpy as np

## Test la methode modulo
print("__methode_modulo__") 
print("3modulo2 : (1?) " +str(E.moduloF(3,2)))
print("3modulo2 : (0.2?) " +str(E.moduloF(3.5,1.1)))     
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
refTerrestre = E.Referentiel("refTerrestre",10,E.Vecteur(1,1,E.ReferentielAbsolu())) 
refAero = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,E.ReferentielAbsolu())) 
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
refTerrestre.setOrigine(E.Vecteur(0,0,E.ReferentielAbsolu()))
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
vecteur1 = E.Vecteur(3,4,refTerrestre)
vecteur2 = E.Vecteur(1,6,refAero)
vecteur3 = E.Vecteur(1,6,refTerrestre)
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
print ("vecteur1 == E.vecteur(3,4,refAero)" + str(vecteur1 == E.Vecteur(3,4,refAero)))
print("\n")
print("__projectionRef__")
print("projection du vecteur1 dans le refAero = vecteur(4,-3,refAero)? ")
print(vecteur1.projectionRef(refAero))
print("si on revient dans le refTerrestre = vecteur(3,4)?")
print(vecteur1.projectionRef(refAero).projectionRef(refTerrestre))
print("\n")
print("__translation__")
print("translation de l'origine du refTerrestre dans le refAero = vecteur(3,5,refAero)? ")
print(vecteur2.translationRef(refTerrestre))
print("translation de l'origine du refTerrestre dans le refAero = vecteur(-5,3,refAero)? ")
print(vecteur1.translationRef(refAero))
print("\n")
print("__changeRef__")
print("Le vecteur1 dans le refAero = vecteur(-1,0,refAero)? ")
print(vecteur1.changeRef(refAero))
print("si on revient dans le refTerrestre = vecteur(3,4)?")
print(vecteur1.changeRef(refAero).changeRef(refTerrestre))
print("Le vecteur2 dans le refTerrestre = vecteur(-3,6,refAero)?")
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
print("le produit vectoriel de vecteur1 et vecteur3 = 14?")
print(vecteur1.prodVect(vecteur3))
print("le produit vectoriel de vecteur2 et vecteur2 = 27?")
print(vecteur1.prodVect(vecteur2))
print("\n")
print("__norm__ + __afficheNorm__")
print("la norme du vecteur1 est egal a 5 dans refterrestre: ?")
vecteur1.afficheNorm(refTerrestre)
print("la norme du vecteur1 est egal a 5 dans refAero: ?")
vecteur1.afficheNorm(refAero)
print("\n")
print("unitaire")
print("vecteur unitaire de (0,0), (1,0) par def ? :" + str(E.Vecteur(0,0,refTerrestre).unitaire()))
print("vecteur unitaire de vecteur1 , (0.6,0.8)? " +str(vecteur1.unitaire()))
