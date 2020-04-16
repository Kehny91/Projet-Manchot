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
print("Je devrais trouver une vitesse de (1 , -2) /!\ sens horaire")
vecteurLiantCGauPoint = Vecteur(1,0,referentielCorps)
#on cree un rigid body pour trouver la vitesse en ce point
point = S.CorpsRigide(vecteurLiantCGauPoint,corps)
corps.addAttachement(point)
#Du coup comme ce le torseur cinetique n est pas bien definis tu ne peux pas utiliser changementPoint Uniquement changementPoint
#On ne peut pas trouver la vitesse d'un point sans en faire un corpsrigide et c'est bien con sniff 

#print("Torseur Cinematique au point = ", corps.getTorseurCinematique().changePoint(vecteurLiantCGauPoint))

#maintenant on peut trouver la vitesse
print("Torseur Cinematique au point = ", point.getVitesse())
print("chouette")
print("")
#Ha oups deja fais avant :/ Bon on reprend avec att
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
# /!\ on ne deplece pas le vecteur mais l'origine du ref associe au coprs quand on deplace le corps

#print("Deplacement du corps en 15,12")
#corps.setTorseurCinematique(Torseur(Vecteur(15,12),Vecteur(1,-1),1)) """

#Ceci revient a utiliser la methode implementee dans planeur (setPosition) elle s'exprime comme ça
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
#ca marche mieux !!

#Enfaite ton vecteur position dans torseurcinematque doit toujours etre Vecteur(0,0,refCorps)
#si tu veux le bouger tu touches a refCorps.origine
# C'est effectivement pas tres pratique mais ca nous permet d ultiliser les torseurs ce qui sera bien en 3D