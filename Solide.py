import Espace as E
import Torseur as T
import numpy as np
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM
import Parametres as P



refTerrestre = E.Referentiel("refTerrestre",0,E.Vecteur(0,0,E.ReferentielAbsolu())) 
refAvion = E.Referentiel("refAvion",0,E.Vecteur(13,15,refTerrestre)) 
#refAero = E.Referentiel("refAero",0,E.Vecteur(0,0,refAvion)) 
refAero = E.Referentiel("refAero",0,E.Vecteur(13,15,refTerrestre)) 


class Corps:
    """classe Corps
    permet de definir un le corps du planeur, le torseur cinematique est donnee au centre de gravite
    \n attribute T.Torseur : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation au centre de gravite
    \n attribute float :  masse, masse de la structure 
    \n attribute float :  inertie, inertie du solide sur l'axe Y au centre de gravite
    \n attribute list : attachement, liste de solides relies a ce corps
    """
    #Init
    def __init__(self, torseurCinetique = T.Torseur(), masse = 0, inertie = 0):
        self.torseurCinematique = torseurCinetique
        self.masse = masse
        self.inertie = inertie
        self.father = None
        self.attachements = []
        self.corpsRigides = [] #ATTENTION, UN CORPS RIGIDE DOIT ETRE DANS LES DEUX LISTES
    #Geter/Seter

    def getTorseurCinematique(self):
        """return le torseurCinematique au centre de gravite dans le refAvion"""
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

    def addCorpsRigide(self, cr):
        self.addAttachement(cr)
        self.corpsRigides.append(cr)
    
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


class Attachements:
    """classe Attachements
    \n attribute E.Vecteur : position, position du solide
    \n attribute float :  masse, masse du solide 
    \n attribute float :  inertie, inertie du solide
    """
    #Init
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0,father = None):
        self.position = position
        self.masse = masse
        self.inertie = inertie
        self.father = father

    #Geter/Seter
    def getPosition(self):
        """return la position du point dans le refAvion"""
        return self.position
    
    def setPosition(self,newPosition):
        self.position = newPosition

    def getVitesse(self):
        """return la vitesse du point dans le refTerrestre"""
        vitessex =  self.father.getTorseurCinematique().resultante.projectionRef(refTerrestre).x + self.father.getTorseurCinematique().moment * self.position.projectionRef(refTerrestre).z
        vitessez =  self.father.getTorseurCinematique().resultante.projectionRef(refTerrestre).z- self.father.getTorseurCinematique().moment * self.position.projectionRef(refTerrestre).x
        return E.Vecteur(vitessex,vitessez,refTerrestre)

    def getMasse(self):
        return self.masse

    def setMasse(self,newMasse):
        self.masse=newMasse

    def getInertie(self):
        return self.inertie

    def setInertie(self,newInertie):
        self.masse=newInertie
    

class Propulseur(Attachements):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, throttle = 0, throttleMax = 0):
        super().__init__(position, masse, inertie, father)
        self.throttle = throttle
        self.throttleMax = throttleMax

    
    def setThrottlePercent(self, throttlePercent):
        self.throttle = self.throttleMax*throttlePercent

    def getTorseurEffortsAttachement(self):

        #Poussee, ne prend pas en compte la montee ne puisance (puissance instantannee) = moteur tres reactif
        torseurPoussee = T.Torseur(self.position,E.Vecteur(self.throttle,0,refAvion),0)
        return torseurPoussee

class SurfacePortante(Attachements):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0):
        super().__init__(position , masse, inertie, father)
        self.S = S
        self.CzA = CzA
        self.Alhpa_0 = Alhpa_0
        self.Cx0 = Cx0
        self.k = k
    
    def getCz(self,Alpha):
        return self.CzA*(Alpha - self.Alhpa_0)

    def getTorseurLift(self,Alpha,V):
        lift = 0.5 * CE.rho_air_0 * self.getCz(Alpha) * V**2
        if V <10:
            return T.Torseur(self.position.changeRef(refAero),E.Vecteur(0,lift,refAero),0)
        else:
            return T.Torseur(self.position.changeRef(refAero),E.Vecteur(0,0,refAero),0)
    
    def getCx(self,Alpha):
        return self.Cx0 + self.k*self.getCz(Alpha)**2

    def getTorseurDrag(self,Alpha,V):
        drag = 0.5 * CE.rho_air_0 * self.getCx(Alpha) * V**2
        return T.Torseur(self.position.changeRef(refAero),E.Vecteur(drag,0,refAero),0)

class Aile(SurfacePortante):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0, angleAileron = 0, pourcentageAileron = 0):
        super().__init__(position , masse, inertie, father, S, CzA, Alhpa_0, Cx0 , k )
        self.angleAileron = angleAileron
        self.pourcentageAileron = pourcentageAileron
    
    def setangleAileron(self, angleAileron):
        self.angleAileron = angleAileron

    def getAlpha(self):
        incidence = self.getVitesse().arg()
        refAero.setOrigine(refAvion.getOrigine())
        refAero.setAngleAxeY(incidence)
        return  self.getVitesse().arg() + self.angleAileron*P.TORAD*self.pourcentageAileron
        
    def getTorseurEffortsAttachement(self):
        V = self.getVitesse().norm()
        alpha = self.getAlpha()
        torseurLift = self.getTorseurLift(alpha,V)
        torseurDrag = self.getTorseurDrag(alpha,V)
        #print(alpha)
        #print (V)
        torseurTot = (torseurDrag + torseurLift)
        print (torseurTot.changeRef(refTerrestre))
        return torseurLift + torseurDrag


class Empennage(SurfacePortante):
    def __init__(self,position = E.Vecteur(), masse = 0, inertie = 0, father = None, S=0, CzA=0, Alhpa_0 = 0, Cx0 = 0, k=0, angleEmpennage = 0, pourcentageEmpennage = 0):
        super().__init__(position , masse, inertie, father, S, CzA, Alhpa_0, Cx0 , k )
        self.angleEmpennage = angleEmpennage
        self.pourcentageEmpennage = pourcentageEmpennage
    
    def setangleEmpennage(self, angleEmpennage):
        self.angleEmpennage = angleEmpennage

    def getAlpha(self):
        incidence = self.getVitesse().arg()
        refAero.setAngleAxeY(incidence)
        return incidence + self.angleEmpennage*P.TORAD*self.pourcentageEmpennage
        
    def getTorseurEffortsAttachement(self):
        V = self.getVitesse().norm()
        alpha = self.getAlpha()
        torseurLift = self.getTorseurLift(alpha,V)
        torseurDrag = self.getTorseurDrag(alpha,V)
        return torseurLift + torseurDrag



#Utilisation:
# 1) Calculer et mettre a jour la vitesse et w du corps entier, avec les corpsRigides désactivé.
# 2) Set le DT de tous les corps rigides
# 3) Tant que tous les corps rigides ne sont pas "ok", recalculer et mettre a jour la vitesse et w
# 4) Reset les corps rigides
class CorpsRigide(Attachements):
    def __init__(self, position, father, referentielSol, epsilon):
        super().__init__(self, position, 0, 0, father)
        self._thisTurnTotalForce = 0
        self._epsilon = epsilon
        self._referentielSol = referentielSol
        self._axeXSol = referentielSol.getAxeX()
        self._axeZSol = referentielSol.getAxeZ()
        self._dt = 0.001
        self._active = False

    def setDt(self,dt):
        self._dt = dt

    def _m0(self):
        #deltaX est censé etre la distance CG -> self, projetée sur l'axe X du sol !
        deltaX = self.getPosition().projectionRef(self._referentielSol).prodScal(self._axeXSol)
        return 1/self.father.getMasseTotal() + (deltaX**2)/self.father.getInertieTotal()

    def reset(self):
        self._thisTurnTotalForce = 0
        self._active = False

    def activer(self):
        self._active = True

    def _underground(self):
        return self.getPosition().changeRef(self._referentielSol).getZ()>0

    def ok(self):
        if (not self._underground()) or (not self._active):
            return True #Si on est au dessus du sol, pas de problème
        #Sinon
        return abs(self.getVitesse().getZ())<self._epsilon

    def getTorseurEffortsAttachement(self):
        """Le dt doit etre celui qui sera utilisé pour l'intégration de la vitesse"""
        if (not self._underground()) or (not self._active):
            return T.Torseur(self.getPosition())
        #Sinon
        F = -1*self.getVitesse().getZ()*self._m0()/self._dt
        #La force totale appliquée ne peut pas etre négative, donc au minimum, F peut valoir -thisTurnTotalForce
        F = max(-1*self._thisTurnTotalForce,F)
        self._thisTurnTotalForce += F
        return T.Torseur(self.getPosition(),E.Vecteur(0,F,self._referentielSol),0)

        #Poids
        torseurPoids=self.getTorseurPoids()
        #Poussee, ne prend pas en compte la montee ne puisance (puissance instantannee) = moteur tres reactif
        torseurPoussee = T.Torseur(self.position,E.Vecteur(0,0,refAvion),0)
        #Somme
        return torseurPoussee + torseurPoids
    
class Planeur():
    def __init__(self):
        self.structure = Corps(T.Torseur(E.Vecteur(0,0,refAvion),E.Vecteur(0,0,refAvion),0),PM.masseTotal,PM.inertieTotal)         
        self.propulseur = Propulseur(E.Vecteur(PM.engine_x,PM.engine_z, refAvion),0,0,self.structure,0,PM.engineMaxThrust)
        self.structure.addAttachement(self.propulseur)
        self.aileD = Aile(E.Vecteur(PM.ailesD_x_Foyer,PM.ailesD_z_Foyer,refAvion), 0, 0, self.structure, PM.aileD_S, PM.aileD_CzA, PM.aileD_Alpha_0, PM.aileD_Cx0, PM.aileD_k, 0, PM.flapsDPourcentage)
        self.structure.addAttachement(self.aileD)
        self.aileG = Aile(E.Vecteur(PM.ailesG_x_Foyer,PM.ailesG_z_Foyer,refAvion), 0, 0, self.structure, PM.aileG_S, PM.aileG_CzA, PM.aileG_Alpha_0, PM.aileG_Cx0, PM.aileG_k, 0, PM.flapsGPourcentage)
        self.structure.addAttachement(self.aileG)
        self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_Foyer,PM.empennageD_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageD_S,PM.empennageD_CzA, PM.empennageD_Alpha_0, PM.empennageD_Cx0, PM.empennageD_k,0 ,PM.elevDMaxAnglePourcentage)
        self.structure.addAttachement(self.empennageD)
        self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_Foyer,PM.empennageG_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageG_S,PM.empennageG_CzA, PM.empennageG_Alpha_0, PM.empennageG_Cx0, PM.empennageG_k,0 ,PM.elevGMaxAnglePourcentage)
        self.structure.addAttachement(self.empennageG)


    ##/!\ origine de l'avion dans l'interface prise au bati moteur
    def getPosition(self):
        return self.propulseur.getPosition().changeRef(refTerrestre)

    def setPosition(self, newPosition):
        self.structure.torseurCinematique.vecteur.ref.setOrigine(newPosition-self.propulseur.position)
        refAero.setOrigine(newPosition-self.propulseur.position)
    
    def getAssiette(self):
        return self.structure.getTorseurCinematique().vecteur.ref.getAngleAxeY()

    def setAssiette(self, newAssiete):
        self.structure.getTorseurCinematique().vecteur.ref.setAngleAxeY(newAssiete)
        

    def getVitesse(self):
        return self.propulseur.getVitesse()
    
    def setVitesse(self, newVitesse):
        vitessex =  newVitesse.x - self.structure.getTorseurCinematique().moment * self.propulseur.position.projectionRef(refTerrestre).z
        vitessez =  newVitesse.z - self.structure.getTorseurCinematique().moment * self.propulseur.position.projectionRef(refTerrestre).x
        return self.structure.getTorseurCinematique().setResultante(E.Vecteur(vitessex,vitessez,refTerrestre))
    
    def diffuseDictRawInput(self,rawInputDict):
        self.propulseur.setThrottlePercent(rawInputDict["throttle"])
        self.aileD.setangleAileron(rawInputDict["flapsD"])
        self.aileG.setangleAileron(rawInputDict["flapsG"])
        self.empennageD.setangleEmpennage(rawInputDict["elevD"])
        self.empennageG.setangleEmpennage(rawInputDict["elevG"])
        

"""     def getPosition(self):
        return self.structure.getTorseurCinematique().vecteur.changeRef(refTerrestre)
    
    def setPosition(self, newPosition):
        self.structure.torseurCinematique.vecteur.ref.setOrigine(newPosition)
    
    def getAssiette(self):
        return self.structure.getTorseurCinematique().vecteur.ref.getAngleAxeY()

    def setAssiette(self, newAssiete):
        self.structure.getTorseurCinematique().vecteur.ref.setAngleAxeY(newAssiete)

    def getVitesse(self):
        return self.structure.getTorseurCinematique().resultante.projectionRef(refTerrestre)
    
    def setVitesse(self, newVitesse):
        return self.structure.getTorseurCinematique().setResultante(newVitesse)
 """
    


       
    