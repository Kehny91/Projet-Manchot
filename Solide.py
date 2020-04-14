import Espace as E
import Torseur as T
import numpy as np

rho_air_0 = 1.225 #kg/m3, masse volumique de l air a une altitude nulle
g_0 = 9.81 #m.s-2, acceleration de pesenteur a altitude nulle

refTerrestre = E.Referentiel("refTerrestre",10,E.Vecteur(1,1,E.ReferentielAbsolu())) 
refAero = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,E.ReferentielAbsolu())) 
refAvion = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,E.ReferentielAbsolu())) 

"""classe Solide
    permet de definir un solide
    attribute T.Torseur : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation au point ou le solide se trouve
    attribute float :  masse, masse du solide 
    attribute float :  inertie, inertie du solide
    attribute list : attachement, liste de solides relies a ce solide
"""
class Solide:
    #Init
    def __init__(self, torseurCinetique = T.Torseur(), masse = 0, inertie = 0):
        self.torseurCinetique = torseurCinetique
        self.masse = masse
        self.inertie = inertie
        self.father = None
        self.attachements = []
    #Geter/Seter

    def getPosition(self):
        return self.torseurCinematique.vecteur
    
    def setPosition(self,newPosition):
        self.torseurCinematique.vecteur = newPosition

    def getTorseurCinematique(self):
        return self.torseurCinematique

    def setTorseurCinematique(self,newTorseurCinematique):
        self.torseurCinematique = newTorseurCinematique
    
    def getMasse(self):
        return self.masse

    def setMasse(self,newMasse):
        self.masse=newMasse
    
    def getMasseTotal(self):
        massetot = self.masse
        for p in self.attachements:
            massetot += p.masse
        return massetot

    def getInertie(self):
        return self.inertie

    def setInertie(self,newInertie):
        self.masse=newInertie
    
    def getInertieTotal(self):
        inertietot = self.inertie
        for p in self.attachements:
            vecteurAB = self.torseurCinematique.vecteur.pointToVect(p.torseurCinematique.vecteur)
            inertietot += p.inertie + p.masse* (vecteurAB.x**2 + vecteurAB.z**2)
        return inertietot

    def addattachement(self,solide):
        self.attachements.append(solide)
        solide.father = self
    
    def updateCinematic(self,dt):
        torseurEfforts = self.computeTorseurEfforts()
        #PFD
        accX = torseurEfforts.resultante.x/self.getMasseTotal()- self.torseurCinematique.moment*self.torseurCinematique.resulante.z
        accZ = torseurEfforts.resultante.z/self.getMasseTotal() + self.torseurCinematique.moment*self.torseurCinematique.resulante.x
        wpoint = torseurEfforts.moment/self.getInertieTotal
        #construction vecteur acceleration
        torseurAcc= T.Torseur(self.torseurCinematique.vecteur,E.Vecteur(accX,accZ,self.torseurCinematique.vecteur.ref),wpoint)
        #update
        self.torseurCinematique += torseurAcc*dt
        self.torseurCinematique.vecteur += E.Vecteur(self.torseurCinematique.resulante)*dt
        self.torseurCinematique.vecteur.ref.setAngleAxeY = torseurAcc.moment*dt

    def computeTorseurEfforts(self):
        torseurEfforts = self.getTorseurPoids()
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement()
            torseursEfforts += torseurEffortsAttachements
        return torseurEfforts

    def getTorseurPoids(self):
        #Poids
        return T.Torseur(self.torseurCinematique.vecteur,E.Vecteur(0,-self.masse * g_0,refTerrestre),0)

class Propulseur(Solide):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0 , throttlemax = 4):
        super().__init__(self, torseurPosition, torseurCinetique, masse)
        self.throttle = 0
        self.throttleMax = throttlemax

    def setThrottlePercent(self, throttlePercent):
        self.throttle = self.throttleMax*throttlePercent

    def getTorseurEffortsAttachement(self):
        #Poids
        torseurPoids=self.getTorseurPoids()
        #Poussee, ne prend pas en compte la montee ne puisance (puissance instantannee) = moteur tres reactif
        torseurPoussee = T.Torseur(self.torseurCinematique.vecteur,E.Vecteur(self.throttle,0,refAvion),0)
        #Somme
        return torseurPoussee + torseurPoids

class Aile(Solide):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0):
        super().__init__(self,torseurPosition, torseurCinetique , masse)
        self.S = S
        self.CzA = CzA
        self.Alhpa_0 = Alhpa_0
        self.Cx0 = Cx0
        self.k = k

    def Cz(self,Alpha):
        return self.CzA*(Alpha - self.Alhpa_0)

    def getTorseurLift(self,Alpha,V):
        
        lift = 0.5 * rho_air_0 * V**2 *self.Cz(Alpha)
        return T.Torseur(self.torseurCinematique.vecteur,E.Vecteur(0,lift,refAero),0)
    
    def Cx(self,Alpha):
        return self.Cx0 + self.k*self.Cz(Alpha)**2

    def getTorseurDrag(self,Alpha,V):
        drag = 0.5 * rho_air_0 * V**2 *self.Cx(Alpha)
        return T.Torseur(self.torseurCinematique.vecteur,E.Vecteur(drag,0,refAero),0)
    
    def getTorseurEffortsAttachement(self,Alpha,V):
        torseurPoids = self.getTorseurPoids()
        torseurLift = self.getTorseurLift(Alpha,V)
        torseurDrag = self.getTorseurDrag(Alpha,V)
        return torseurLift + torseurDrag + torseurPoids

class Aileron(Aile):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0, angleAilerons =0):
        super.__init__(self, torseurPosition, torseurCinetique, masse, S, CzA, Alhpa_0, Cx0, k)
        self.angleaAileron = angleAilerons

class Empenage(Aile):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0):
        super.__init__(self, torseurPosition, torseurCinetique, masse, S, CzA, Alhpa_0, Cx0, k)

class Gouverne(Aile):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0, angleGouverne =0):
        super.__init__(self, torseurPosition, torseurCinetique, masse, S, CzA, Alhpa_0, Cx0, k)
        self.angleaGouverne = angleGouverne
