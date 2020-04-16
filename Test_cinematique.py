import Solide as S
from Torseur import Torseur
from Espace import Vecteur,Referentiel
print("Creation d'un corps")
corps = S.Corps()

print("Deplacement en 10 10 avec une vitesse 1 -1 et un W de 1rad/s")
#                                   | Position   |   Vitesse    |W|
corps.setTorseurCinematique(Torseur(Vecteur(10,10),Vecteur(1,-1),1))
referentielCorps = Referentiel("refCorps",0,Vecteur(10,10))

print("Torseur Cinematique = ", corps.getTorseurCinematique())
print("")

print("Je veux maintenant connaitre la vitesse d'un point de ce solide sité a 1 0 du CG")
print("Je devrais trouver une vitesse de (1 , -2) /!\ sens horaire")
vecteurLiantCGauPoint = Vecteur(1,0,referentielCorps)
print("Torseur Cinematique au point = ", corps.getTorseurCinematique().changePoint(vecteurLiantCGauPoint))
