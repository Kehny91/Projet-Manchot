# -*- coding: utf-8 -*-
"""
Created on Tue Apr 07 14:20:06 2020

@author: tomju
"""

import Torseur as T
import Espace as E
import numpy as np

#test de la classe Point
print("__Classe_Torseur__")
#Constructeur
print("__Init__")

refAero = E.Referentiel("refAero",np.pi/3,E.Vecteur(3,5))
refTerrestre = E.Referentiel("refTerrestre",0,E.Vecteur(0,0))


torseur1 = T.Torseur(E.Vecteur(3,5,refTerrestre), E.Vecteur(1,1,refTerrestre), 8.5)
torseur1bis = T.Torseur()
torseur1bis.init2(1,1,refTerrestre,3,1,8.5)
torseur2 = T.Torseur()
""" torseur2.init2(3,4,refAero,4,5,1.1)
origineRefAero = E.Vecteur(3,5,refTerrestre) """

torseur2.init2(-1.5,0.1,refAero,0,10,0)
origineRefAero = E.Vecteur(0,0,refAero)
#origineRefAero = E.Vecteur(3,5,refTerrestre)

pointA = E.Vecteur(7,1,refAero)
""" print("Init_Fin")
print("\n")
print("__str__")
print(torseur1)
print(torseur1bis)
print(torseur2)
print("\n")
print("__eq__")
print ("torseur1==torseur1 True? " + str(torseur1==torseur1))
print ("torseur1==torseur1bis True? " + str(torseur1==torseur1bis))
print ("torseur1==torseur2 False? " + str(torseur1==torseur2))
print("\n")
print("__changeRef__")
print(torseur1.changeRef(refAero))
print(torseur1.changeRef(refAero).changeRef(refTerrestre))
print("\n")
print("__changePoint__")
print(torseur1.changePoint(pointA))
print(torseur1.changePoint(pointA).changePoint(E.Vecteur(1,1,refTerrestre)))
print("\n")
print("__add__")
print("torseur1 + torseur1 = 2*torseur1? ")
print(torseur1 + torseur1)
print("torseur1 + torseur2 = Torseur(1,1,refTerrestre,2.3,-5.3)? ")
print(torseur1 + torseur2)
print("\n")
print("torseur1 - torseur1 = torseur nul? ")
print(torseur1 - torseur1)
print("torseur1 - torseur2 = Torseur(1,1,refTerrestre,3.6,7.3)? ")
print(torseur1 - torseur2 )
print("\n")
print("__mul__")
print("torseur1*2 = Torseur(1,1,refterrestre,6,2,17)")
print(torseur1*2.)
print("\n")
 """
""" print(origineRefAero.pointToVect(torseur2.vecteur))
print(torseur2.changeRef(refTerrestre)) """
#print(torseur1)
#print(origineRefAero.pointToVect(torseur2.vecteur).prodVect(E.Vecteur(141,141,refTerrestre)))#
print(torseur2.changePoint(origineRefAero))
#print(torseur1 + torseur2.changePoint(origineRefAero))
#print(torseur1 + torseur2)