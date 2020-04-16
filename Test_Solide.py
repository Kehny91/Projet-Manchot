import Espace as E
import Torseur as T
import Solide as S
import numpy as np

""" #Pour les angles utiliser les MDD
refTerrestre = E.Referentiel("refTerrestre",10,E.Vecteur(1,1)) 
refAero = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,)) 
refAvion = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,))
refAileronD = E.Referentiel("refAileronD",refAvion.getAngleAxeY()+0.1*np.pi, E.Vecteur(1,1,refAvion))
refAileronG = E.Referentiel("refAileronG",refAvion.getAngleAxeY()+0.1*np.pi, E.Vecteur(1,1,refAvion))
refGouverneD = E.Referentiel("refGouverneD",refAvion.getAngleAxeY()+0.1*np.pi, E.Vecteur(-1,-1,refAvion))
refGouverneG = E.Referentiel("refGouverneG",refAvion.getAngleAxeY()+0.1*np.pi, E.Vecteur(-1,-1,refAvion))

corps = S.Solide(T.Torseur(E.Vecteur(3,5),E.Vecteur(1,1),0),0.3,0)

aileD = S.Aile(T.Torseur(E.Vecteur(1,1,refAvion),E.Vecteur(0,0),0),0.2,0))
aileronD = S.Aileron(T.Torseur(E.vecteur(0,0,)))

aileG = S.Aile(T.Torseur(E.Vecteur(1,1,refAvion),E.Vecteur(0,0),0),0.2,0)) """
planeur = S.Planeur()
print(planeur.getPosition())
torseurCinematique = T.Torseur(E.Vecteur(1,1,S.refAvion),E.Vecteur(10,0,S.refTerrestre),0)
#print(torseurCinematique.resultante)
planeur.structure.updateCinematique(0.1)
print(planeur.getPosition())
""" print(planeur.structure.computeTorseurEfforts())
print(planeur.propulseur.getTorseurEffortsAttachement())
print(planeur.propulseur.getTorseurEffortsAttachement().changePoint(E.Vecteur(0,0,S.refAvion))) """