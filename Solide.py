import Espace as E
import Torseur as T

rho_air_0 = 1.225 #kg/m3, masse volumique de l air a une altitude nulle
g_0 = 9.81 #m.s-2, acceleration de pesenteur a altitude nulle

refTerrestre = E.Referentiel("refTerrestre",10,E.Vecteur(1,1,E.ReferentielAbsolu())) 
refAero = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,E.ReferentielAbsolu())) 
refAvion = E.Referentiel("refAero",np.pi/2,E.Vecteur(3,5,E.ReferentielAbsolu())) 

"""classe Solide
    permet de definir un solide
    attribute T.Toseur : torseurPosition, determine la position et l'angle du solide dans un referentiel
    attribute T.Torseur : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation
    attribute float :  masse, masse du solide 
    attribute float :  inertie, inertie du solide
    attribute list : attachement, liste de solides relies a ce solide
"""
class Solide:
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0):
        self.torseurPosition = toreurPosition
        self.torseurCinetique = torseurCinetique
        self.masse = masse
        self.inertie = inertie
        self.father = None
        self.attachements = []

    def addattachement(self,solide):
        self.attachement.append(solide)
        solide.father = self
    
    def updateCinematic(self,dt):
        torseurEfforts = self.computeTorseurEfforts()
        #PFD
        accX = torseurEfforts.Resultante.x/self.mass- self.torseurCinematique.moment*self.torseurCinematique.resulante.z
        accZ = torseurEfforts.Resultante.z/self.mass + self.torseurCinematique.moment*self.torseurCinematique.resulante.x
        wpoint = torseurEfforts.moment/self.I
        #construction vecteur acceleration
        torseurAcc= T.Torseur(sef.torseurPosition,E.vecteur=(accX,accZ,self.torseurPosition.vecteur.ref),wpoint)
        #update
        self.torseurCinematique += torseurAcc*dt
        self.torseurPosition += torseurCinematique*dt

    def computeTorseurEfforts(self):
        torseurEfforts = getTorseurPoids()
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement()
            torseursEfforts += torseurEffortsAttachements
        return torseurEfforts

    def getTorseurPoids(self):
        #Poids
        return T.Torseur(self.torseurPosition,E.vecteur=(0,-self.masse * g_0,refTerrestre),0)

class Propulseur(Solide):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0,throttle =0 , throttlemax = 4):
        super().__init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0):
        self.throttle = throttle
        self.throttleMax = throttlemax

    def getTorseurEfforts(self):
        #Poids
        torseurPoids=self.getTorseurPoids()
        #Poussee, ne prend pas en compte la montee ne puisance (puissance instantannee) = moteur tres reactif
        torseurPossee = T.Torseur(self.torseurPosition,E.vecteur=(throttleMax*throttle,0,refAvion),0)
        #Somme
        return TorseurPoussee + torseurPoids

class aile(Solide):
    def __init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0, S=0, CzA=0, Cx0 = 0):
        super().__init__(self,torseurPosition= T.Torseur(),torseurCinetique = T.Torseur(), masse = 0):
        self.S = S
        self.CzA = CzA
        self.Cx0 = Cx0

    def getTorseurLift(self,Alpha):
        
        lift = 0.5 * rho_air_0 
        return T.Torseur(self.torseurPosition,E.vecteur=(0,-self.masse * g,refTerrestre),0)



