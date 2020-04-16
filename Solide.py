import Espace as E
import Torseur as T
import numpy as np
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM



refTerrestre = E.Referentiel("refTerrestre",0,E.Vecteur(0,0,E.ReferentielAbsolu())) 
refAero = E.Referentiel("refAero",np.pi/4,E.Vecteur(3,5,refTerrestre)) 
refAvion = E.Referentiel("refAvion",np.pi/4,E.Vecteur(13,15,refTerrestre)) 

"""classe Corps
    permet de definir un le corps du planeur, le torseur cinematique est donnee au centre de gravite
    attribute T.Torseur : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation au centre de gravite
    attribute float :  masse, masse de la structure 
    attribute float :  inertie, inertie du solide sur l'axe Y au centre de gravite
    attribute list : attachement, liste de solides relies a ce corps
"""
class Corps:
    #Init
    def __init__(self, torseurCinetique = T.Torseur(), masse = 0, inertie = 0):
        self.torseurCinematique = torseurCinetique
        self.masse = masse
        self.inertie = inertie
        self.father = None
        self.attachements = []
    #Geter/Seter

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
            vecteurAB = self.torseurCinematique.vecteur.pointToVect(p.position)
            inertietot += p.inertie + p.masse* (vecteurAB.x**2 + vecteurAB.z**2)
        return inertietot

    def addAttachement(self,solide):
        self.attachements.append(solide)
        solide.father = self
    
    def updateCinematique(self,dt):
        torseurEfforts = self.computeTorseurEfforts()
        #PFD
        accX = torseurEfforts.resultante.x/self.getMasseTotal()- self.torseurCinematique.moment*self.torseurCinematique.resultante.z
        accZ = torseurEfforts.resultante.z/self.getMasseTotal() + self.torseurCinematique.moment*self.torseurCinematique.resultante.x
        wpoint = torseurEfforts.moment/self.getInertieTotal()
        vecteurAcce = E.Vecteur(accX,accZ,refTerrestre)
        #construction vecteur acceleration
        torseurAcc= T.Torseur(self.torseurCinematique.vecteur,vecteurAcce.projectionRef(refAvion),wpoint)
        #update
        self.torseurCinematique += torseurAcc*dt
        self.move(self.torseurCinematique,dt)

    def move(self,torseurCinematique,dt):
        self.torseurCinematique.vecteur.ref.setOrigine(self.torseurCinematique.vecteur.ref.getOrigine() + torseurCinematique.resultante.projectionRef(refTerrestre)*dt)
        self.torseurCinematique.vecteur.ref.setAngleAxeY(self.torseurCinematique.vecteur.ref.getAngleAxeY() + torseurCinematique.moment*dt )

    def computeTorseurEfforts(self):
        torseurEfforts = self.getTorseurPoids()
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement()
            torseurEfforts += torseurEffortsAttachements
        return torseurEfforts

    def getTorseurPoids(self):
        #Poids
        return T.Torseur(self.torseurCinematique.vecteur.changeRef(refTerrestre),E.Vecteur(0,-self.masse * CE.g_0,refTerrestre),0)

"""classe Attachements
    attribute E.Vecteur : position, position du solide
    attribute float :  masse, masse du solide 
    attribute float :  inertie, inertie du solide
"""
class Attachements:
    #Init
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0,father = None):
        self.position = position
        self.masse = masse
        self.inertie = inertie
        self.father = father

    #Geter/Seter
    def getPosition(self):
        return self.position
    
    def setPosition(self,newPosition):
        self.position = newPosition

    def getVitesse(self):
        vitessex =  self.father.getTorseurCinematique().resultante.x + self.father.getTorseurCinematique().moment * self.position.projectionRef(refTerrestre).z
        vitessez =  self.father.getTorseurCinematique().resultante.x- self.father.getTorseurCinematique().moment * self.position.projectionRef(refTerrestre).x
        return E.Vecteur(vitessex,vitessez,refTerrestre)

    def getMasse(self):
        return self.masse

    def setMasse(self,newMasse):
        self.masse=newMasse

    def getInertie(self):
        return self.inertie

    def setInertie(self,newInertie):
        self.masse=newInertie
    
    def getTorseurPoids(self):
        #Poids
        return T.Torseur(self.position,E.Vecteur(0,-self.masse * CE.g_0,refTerrestre),0)

class Propulseur(Attachements):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, throttle = 0, throttleMax = 0):
        super().__init__(position, masse, inertie, father)
        self.throttle = throttle
        self.throttleMax = throttleMax

    def setThrottlePercent(self, throttlePercent):
        self.throttle = self.throttleMax*throttlePercent

    def getTorseurEffortsAttachement(self):
        #Poids
        torseurPoids=self.getTorseurPoids()
        #Poussee, ne prend pas en compte la montee ne puisance (puissance instantannee) = moteur tres reactif
        torseurPoussee = T.Torseur(self.position,E.Vecteur(self.throttle,0,refAvion),0)
        #Somme
        return torseurPoussee + torseurPoids

class Aile(Attachements):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0, angleAileron = 0, pourcentageAileron = 0):
        super().__init__(position , masse, inertie, father)
        self.S = S
        self.CzA = CzA
        self.Alhpa_0 = Alhpa_0
        self.Cx0 = Cx0
        self.k = k
        self.angleAileron = angleAileron
        self.pourcentageAileron = pourcentageAileron

    def Cz(self,Alpha):
        return self.CzA*(Alpha + self.angleAileron*self.pourcentageAileron - self.Alhpa_0)

    def getTorseurLift(self,Alpha,V):
        
        lift = 0.5 * CE.rho_air_0 * V**2 *self.Cz(Alpha)
        return T.Torseur(self.position,E.Vecteur(0,lift,refAero),0)
    
    def Cx(self,Alpha):
        return self.Cx0 + self.k*self.Cz(Alpha)**2

    def getTorseurDrag(self,Alpha,V):
        drag = 0.5 * CE.rho_air_0 * V**2 *self.Cx(Alpha)
        return T.Torseur(self.position,E.Vecteur(drag,0,refAero),0)
    
    def getTorseurEffortsAttachement(self):
        torseurPoids = self.getTorseurPoids()
        V = self.getVitesse().norm()
        torseurLift = self.getTorseurLift(self.father.getTorseurCinematique().vecteur.ref.angleAxeY,V)
        torseurDrag = self.getTorseurDrag(self.father.getTorseurCinematique().vecteur.ref.angleAxeY,V)
        return torseurLift + torseurDrag + torseurPoids

class Empennage(Attachements):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0, angleEmpennage = 0, pourcentageEmpenage = 0):
        super().__init__(position , masse, inertie, father)
        self.S = S
        self.CzA = CzA
        self.Alhpa_0 = Alhpa_0
        self.Cx0 = Cx0
        self.k = k
        self.angleEmpennage = angleEmpennage
        self.pourcentageEmpenage = pourcentageEmpenage
    
    def setangleEmpennage(self, angleEmpennage):
        self.angleEmpennage = angleEmpennage

    def Cz(self,Alpha):
        return self.CzA*(Alpha + self.angleEmpennage*self.pourcentageEmpenage - self.Alhpa_0)

    def getTorseurLift(self,Alpha,V):
        
        lift = 0.5 * CE.rho_air_0 * V**2 *self.Cz(Alpha)
        return T.Torseur(self.position,E.Vecteur(0,lift,refAero),0)
    
    def Cx(self,Alpha):
        return self.Cx0 + self.k*self.Cz(Alpha)**2

    def getTorseurDrag(self,Alpha,V):
        drag = 0.5 * CE.rho_air_0 * V**2 *self.Cx(Alpha)
        return T.Torseur(self.position,E.Vecteur(drag,0,refAero),0)
    
    def getTorseurEffortsAttachement(self):
        torseurPoids = self.getTorseurPoids()
        V = self.getVitesse().norm()
        torseurLift = self.getTorseurLift(self.father.getTorseurCinematique().vecteur.ref.angleAxeY,V)
        torseurDrag = self.getTorseurDrag(self.father.getTorseurCinematique().vecteur.ref.angleAxeY,V)
        return torseurLift + torseurDrag + torseurPoids

class CorpsRigide(Attachements):
    def __init__(self,position = E.Vecteur(), father = None):
        super().__init__(self, position, 0, 0, father)

    def getTorseurEffortsAttachement(self):

        #Poids
        torseurPoids=self.getTorseurPoids()
        #Poussee, ne prend pas en compte la montee ne puisance (puissance instantannee) = moteur tres reactif
        torseurPoussee = T.Torseur(self.position,E.Vecteur(self.throttle,0,refAvion),0)
        #Somme
        return torseurPoussee + torseurPoids
    
class Planeur():
    def __init__(self):
        self.structure = Corps(T.Torseur(E.Vecteur(0,0,refAvion),E.Vecteur(0,0,refAvion),0),PM.masseTotal,PM.inertieTotal)         
        self.propulseur = Propulseur(E.Vecteur(PM.engine_x,PM.engine_z, refAvion),0,0,self.structure,0,PM.engineMaxThrust)
        self.structure.addAttachement(self.propulseur)
  
    def getPosition(self):
        return self.structure.getTorseurCinematique().vecteur.changeRef(refTerrestre)
    
    def setPosition(self, newPosition):
        self.structure.torseurCinematique.vecteur.ref.setOrigine(newPosition)
    
    def getAssiette(self):
        return self.structure.getTorseurCinematique().vecteur.ref.getAngleAxeY()

    def setAssiette(self, newAssiete):
        self.structure.getTorseurCinematique().vecteur.ref.setAngleAxeY(newAssiete)

    def getVitesse(self):
        return self.structure.getTorseurCinematique().resultante.projectionRef(refTerrestre)
    
    def setvitesse(self, newVitesse):
        return self.structure.getTorseurCinematique().setResultante(newVitesse)

    def diffuseDictRawInput(self,rawInputDict):
        self.propulseur.setThrottlePercent(rawInputDict["throttle"])
        return
"""         self.aileD = Aile(E.Vecteur(PM.ailesD_x_Foyer,PM.ailesD_z_Foyer,refAvion), 0, 0, self.structure, PM.aileD_S, PM.aileD_CzA, PM.aileD_Alpha_0, PM.aileD_Cx0, PM.aileD_k, 0, PM.flapsDPourcentage)
        self.aileG = Aile(E.Vecteur(PM.ailesG_x_Foyer,PM.ailesG_z_Foyer,refAvion), 0, 0, self.structure, PM.aileG_S, PM.aileG_CzA, PM.aileG_Alpha_0, PM.aileG_Cx0, PM.aileG_k, 0, PM.flapsGPourcentage)
        self.structure.addAttachement(self.aileD)
        self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_Foyer,PM.empennageD_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageD_S, PM.empennageD_Alpha_0, PM.empennageD_Cx0, PM.empennageD_k,0 ,PM.elevDMaxAnglePourcentage)
        self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_Foyer,PM.empennageG_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageG_S, PM.empennageG_Alpha_0, PM.empennageG_Cx0, PM.empennageG_k,0 ,PM.elevGMaxAnglePourcentage)
        
        self.structure.addAttachement(self.aileD)
        self.structure.addAttachement(self.aileG)
        self.structure.addAttachement(self.empennageD)
        self.structure.addAttachement(self.empennageG) 
"""  
       
    