import Espace as E
import Torseur as T
import Solide as S
import numpy as np


planeur = S.Planeur()
print("flightData")
print(planeur.getPosition())
print(planeur.getAssiette())
print(planeur.getVitesse())
print("set")
planeur.setPosition(E.Vecteur(8,8,S.refTerrestre))
planeur.setAssiette(0.1) 
planeur.setVitesse(E.Vecteur(1,1,S.refTerrestre))
#planeur.getVitesse()
#torseurCinematique = T.Torseur(E.Vecteur(1,1,S.refAvion),E.Vecteur(10,0,S.refTerrestre),0)
#print(torseurCinematique.resultante)
print("vitesseAile")
print(planeur.empennageD.getVitesse())
print("torseurEffort")
print(planeur.aileD.getTorseurEffortsAttachement())
print(planeur.aileD.getTorseurEffortsAttachement().changePoint(E.Vecteur(8,8,S.refAvion)))
print(planeur.structure.computeTorseurEfforts()-planeur.aileD.getTorseurEffortsAttachement())
print("update")
planeur.structure.updateCinematique(0.1)
""" print("flightData")
print(planeur.getPosition())
print(planeur.getAssiette())
print(planeur.getVitesse())
print("vitesseAile")
print(planeur.aileD.getVitesse())
planeur.structure.updateCinematique(0.1)
print("flightData")
print(planeur.propulseur.getVitesse())
print(planeur.getPosition())
print(planeur.getAssiette())
print(planeur.getVitesse()) """