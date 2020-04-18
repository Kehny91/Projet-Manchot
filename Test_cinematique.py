import Solide as S
from Torseur import Torseur
from Espace import Vecteur,Referentiel,ReferentielAbsolu


print("Creation d'un corps")
corps = S.Corps()
refTerrestre = Referentiel("refterrestre", 0,Vecteur(0,0))

#Correction
#print("Deplacement en 10 10 avec une vitesse 1 -1 et un W de 1rad/s")
#                                   | Position   |   Vitesse    |W|

#corps.setTorseurCinematique(Torseur(Vecteur(10,10),Vecteur(1,-1),1)) la ton corps n est pas superpose avec le ref
print("POSITION en 10 10 avec une vitesse 1 -1 et un W de 1rad/s")
referentielCorps = Referentiel("refCorps",0,Vecteur(10,10)) #position du ref est a 10,10 du refAbs
corps.setTorseurCinematique(Torseur(Vecteur(0,0,referentielCorps),Vecteur(1,-1),1))

print("Torseur Cinematique = ", corps.getTorseurCinematique())
print("")
print("Je veux maintenant connaitre la vitesse d'un point de ce solide sité a 1 0 du CG")
vecteurLiantCGauPoint = Vecteur(1,0,referentielCorps)
print("Creation d'un attachement au point précédant")
att = S.Attachements(vecteurLiantCGauPoint,father=corps)
print("")
print("Lecture de sa position dans le ref avion normalement (1,0)")
print(att.getPosition())
print("")
print("Lecture de sa position dans le ref abs normalement (11,10)")
print(att.getPosition().changeRef(ReferentielAbsolu()))
print("")
print("Lecture de sa vitesse normalement (1,-2) /!\ sens horaire")
print(att.getVitesse())
print("")
print("Deplacement du corps en 15,12")
corps.getTorseurCinematique().vecteur.ref.setOrigine(Vecteur(15,12))
print("Torseur Cinematique = ", corps.getTorseurCinematique())
print("Torseur Cinematique refTerrestre = ", corps.getTorseurCinematique().changeRef(refTerrestre))
print("")
print("Lecture de la pos de l'attachement")
print("Lecture de sa position dans le ref avion normalement (1,0)")
print(att.getPosition())
print("")
print("Lecture de sa position dans le ref abs normalement (16,12)")
print(att.getPosition().changeRef(ReferentielAbsolu()))

print("========TORSEUR=======")
print("Creation d'un torseur a l'attachement avec fx = 0 et fz = 1")
tor = Torseur(vecteurLiantCGauPoint,Vecteur(0,1,referentielCorps))
print(tor)
print("Depalcement a l'origine du corps on devrait maintenant avoir un moment negatif (sens horaire)")
print(tor.changePoint(corps.getTorseurCinematique().getVecteur()))

print("Deplacement du corps en 10,12")
corps.getTorseurCinematique().vecteur.ref.setOrigine(Vecteur(10,12))
print(tor)
print(tor.getVecteur().changeRef(refTerrestre))
print("")
print("Rotation du corps de pi/2")
corps.getTorseurCinematique().vecteur.ref.setAngleAxeY(3.1415/2)
print("Lecture de la vitesse du corps. Normalement toujours 1 -1 dans ref terrestre")
print(corps.getTorseurCinematique().getResultante().projectionRef(refTerrestre))
print("Lecture de la position de l'att dans le ref avion normalement (1,0)")
print(att.getPosition())
print("Lecture de la position de l'att dans le ref abs normalement (10,11)")
print(att.getPosition().changeRef(ReferentielAbsolu()))
print("vitesse de l'att dans ref terrestre normalement (0,-1)")
print(att.getVitesse())
print("Affichage du torseur au CG")
print(tor.changePoint(corps.getTorseurCinematique().getVecteur()))

print("==== VECTEUR COPY ====")
"""
torseur1 = Torseur(Vecteur(0,0,referentielCorps),Vecteur(0,1,referentielCorps),0)
print("torseur1 ",torseur1)
torseur2 = torseur1 * 2
torseur2 = torseur2.changePoint(Vecteur(1,1))
print("")
print("torseur1 ",torseur1)
print("torseur2 ",torseur2) 
torseur2 = torseur2.changeRef(refTerrestre)
print("")
print("torseur1 ",torseur1)
print("torseur2 ",torseur2) 
torseur2 += torseur1
print("")
print("torseur1 ",torseur1)
print("torseur2 ",torseur2) 
"""
torseur1 = Torseur(Vecteur(0,0,referentielCorps),Vecteur(0,1,referentielCorps),0)
print(" ini torseur1",torseur1)
print(" ini torseur1 refT",torseur1.changeRef(refTerrestre))
torseur2 = Torseur(Vecteur(0,0,referentielCorps),Vecteur(10,10,referentielCorps),0)
torseur3 = torseur1 + torseur2 # Torseur 3 a peut etre son vecteur qui est lié a torseur 1
torseur3.vecteur.ref.setOrigine(Vecteur(15,15,refTerrestre))
print("")
print(" fin torseur1",torseur1)
print(" fin torseur1 refT",torseur1.changeRef(refTerrestre))