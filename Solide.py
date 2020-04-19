import Espace as E
import Torseur as T
import numpy as np
from Polaire import PolaireLineaire,PolaireTabulee
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM
from Parametres import ParametresSimulation as PS
import Parametres as P
from DataTypes import RapportDeCollision
from DataManagement import normalize



refTerrestre = E.Referentiel("refTerrestre",0,E.Vecteur(0,0,E.ReferentielAbsolu())) 
refAvion = E.Referentiel("refAvion",0,E.Vecteur(0,0,refTerrestre)) 
refAero = E.Referentiel("refAero",0,E.Vecteur(0,0,refTerrestre)) 


class Corps:
    """classe Corps
    permet de definir un le corps du planeur, le torseur cinematique est donnee au centre de gravite
    \n attribute T.Torseur : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation au centre de gravite
    \n attribute float :  masse, masse de la structure 
    \n attribute float :  inertie, inertie du solide sur l'axe Y au centre de gravite
    \n attribute list : attachement, liste de solides relies a ce corps
    """
    #Init
    def __init__(self, torseurCinetique , world, masse = 0, inertie = 0):
        self.world = world
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

    def deactivateAllCorpsRigide(self):
        for cr in self.corpsRigides:
            cr.reset()

    def activateAllCorpsRigides(self, dt):
        for cr in self.corpsRigides: 
            cr.activer()
            cr.setDt(dt)
    
    def corpsRigideOk(self):
        for cr in self.corpsRigides:
            if not cr.ok():
                return False
        return True

    def applyAction(self, torseurAction, totMass, totInertie, dt):
        """ Modifie le torseur cinematique"""
        torseurCin = self.getTorseurCinematique()
        torseurAction = torseurAction.changePoint(torseurCin.vecteur)
        torseurCin.setResultante(torseurCin.getResultante() + torseurAction.getResultante()*(dt/totMass))
        torseurCin.setMoment(torseurCin.getMoment() + torseurAction.getMoment()*(dt/totInertie))
    
    def update(self,dt):
        self.deactivateAllCorpsRigide()
        torseurEfforts = self.computeTorseurEfforts().changePoint(self.torseurCinematique.vecteur) # C'est mieux de faire le PFD au CG...
        self.applyAction(torseurEfforts, self.getMasseTotal(), self.getInertieTotal(), dt)

        self.activateAllCorpsRigides(dt)
        
        i=0
        while (not self.corpsRigideOk()):
            torseurEffortsCollisions = T.Torseur(self.torseurCinematique.vecteur)
            for cr in self.corpsRigides:
                torseur = cr.getTorseurEffortsAttachement()
                torseurEffortsCollisions += torseur.changePoint(self.torseurCinematique.vecteur)
            self.applyAction(torseurEffortsCollisions, self.getMasseTotal(), self.getInertieTotal(), dt)
            i+=1
            if (i==100):
                assert False
        
        self.updatePosAndAssiette(dt)

    def generateRapportCollision(self):
        out = RapportDeCollision()
        for cr in self.corpsRigides:
            if cr._thisTurnTotalForce > 0:
                out.addImpact(cr.position.changeRef(refTerrestre),E.Vecteur(cr._thisTurnTotalForceX,cr._thisTurnTotalForce,refTerrestre))
        return out


    def updatePosAndAssiette(self,dt):
        #print("W = ",torseurCinematique.moment)
        self.torseurCinematique.vecteur.ref.setOrigine(self.torseurCinematique.vecteur.ref.getOrigine() + self.torseurCinematique.resultante.projectionRef(refTerrestre)*dt)
        self.torseurCinematique.vecteur.ref.setAngleAxeY(self.torseurCinematique.vecteur.ref.getAngleAxeY() + self.torseurCinematique.moment*dt )

    def computeTorseurEfforts(self):
        torseurEfforts = self.getTorseurPoids().changePoint(self.torseurCinematique.vecteur)
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement().changePoint(self.torseurCinematique.vecteur)           
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
        BA = self.father.getTorseurCinematique().vecteur.pointToVect(self.position).projectionRef(refTerrestre)
        vitessex =  self.father.getTorseurCinematique().resultante.projectionRef(refTerrestre).x + BA.z * self.father.getTorseurCinematique().moment
        vitessez =  self.father.getTorseurCinematique().resultante.projectionRef(refTerrestre).z - BA.x * self.father.getTorseurCinematique().moment 
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
        #print(torseurPoussee)
        return torseurPoussee

class SurfacePortante(Attachements):
    def __init__(self, position, polaire, S, corde, masse = 0, inertie = 0, father = None):
        super().__init__(position , masse, inertie, father)
        self.S = S
        self.polaire = polaire
        self.corde = corde
    
    def getResultanteAero(self, alpha, VrefSol): #Permet de ne pas creer puis sommer les torseur
        VecteurXaeroLocal = VrefSol.unitaire()
        VecteurZaeroLocal = VecteurXaeroLocal.rotate(-np.pi/2)  
        v = VrefSol.norm()
        Fdyn = 0.5 * CE.rho_air_0 *self.S*(v**2)
        lift = Fdyn*self.polaire.getCl(alpha,v)
        drag = Fdyn*self.polaire.getCd(alpha,v)
        #moment = Fdyn*self.polaire.getCm(alpha,v)*self.corde
        moment = 0
        vectAero = VecteurXaeroLocal + VecteurZaeroLocal
        forceAero = E.Vecteur(vectAero.projectionRef(refAvion).x*(-1*drag), vectAero.projectionRef(refAvion).z*lift, refAvion)
        
        return T.Torseur(self.position.changeRef(refAvion),forceAero,moment)
        ####forceAeroRefSol = VecteurXaeroLocal*(-1*drag) + VecteurZaeroLocal*lift
        #print("forceAero")
        #print(forceAeroRefSol)
        ####return T.Torseur(self.position.changeRef(refAvion),forceAeroRefSol.projectionRef(refAvion),moment)

    #TODO Tom. Attention, alpha c'est bien une différence d'angle entre l'angle du fuselage et l'angle de la vitesse
    def getAlpha(self, VrefSol):
        #print("Assiette = ",refAvion.getAngleAxeY())
        return normalize(VrefSol.projectionRef(refAvion).arg())


class Aile(SurfacePortante):
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxFlaps, world, masse = 0, inertie = 0, father = None):
        super().__init__(position, polaire , S, corde, masse, inertie, father)
        self.angleFlaps = 0
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.angleMaxFlaps = angleMaxFlaps
        self.world = world
    
    def setBraquageFlaps(self, pourcentageBraquageFlaps):
        self.angleFlaps = pourcentageBraquageFlaps*self.angleMaxFlaps

    def getAlpha(self, VrefSol):
        alphaFixe = super().getAlpha(VrefSol) #Appelle SurfacePortante.getAlpha()
        theta = self.angleFlaps
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = np.arctan2(np.sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + np.cos(theta))
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        vLoc = self.getVitesse() - self.world.getVent(self.getPosition().changeRef(refTerrestre))
        (alphaFixe,gainAlpha) = self.getAlpha(vLoc)
        torseurFixe = self.getResultanteAero(alphaFixe, vLoc)*(1 - self.pourcentageEnvergureArticulee)
        torseurFlaps = self.getResultanteAero(normalize(alphaFixe + gainAlpha),vLoc)*self.pourcentageEnvergureArticulee
        torseurTot = torseurFixe + torseurFlaps
        return torseurTot


class Empennage(SurfacePortante):
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxGouverne, world, masse = 0, inertie = 0, father = None):
        super().__init__(position, polaire , S, corde, masse, inertie, father)
        self.angleGouverne = 0
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.angleMaxGouverne = angleMaxGouverne
        self.world = world
    
    def setBraquageGouverne(self, pourcentageBraquageGouverne):
        self.angleGouverne = pourcentageBraquageGouverne*self.angleMaxGouverne

    def getAlpha(self, VrefSol):
        alphaFixe = super().getAlpha(VrefSol) #Appelle SurfacePortante.getAlpha()
        theta = self.angleGouverne
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = np.arctan2(np.sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + np.cos(theta))
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        vLoc = self.getVitesse() - self.world.getVent(self.getPosition().changeRef(refTerrestre))
        (alphaFixe,gainAlpha) = self.getAlpha(vLoc)
        torseurFixe = self.getResultanteAero(alphaFixe,vLoc)*(1 - self.pourcentageEnvergureArticulee)
        torseurGouverne = self.getResultanteAero(normalize(alphaFixe + gainAlpha),vLoc)*self.pourcentageEnvergureArticulee
        torseurTot = torseurFixe + torseurGouverne
        #print("emp v = ",v,"alpha = ", alphaFixe + gainAlpha," fzavion = ",torseurTot.getResultante().projectionRef(refAvion).getZ()," fxavion = ", torseurTot.getResultante().projectionRef(refAvion).getX(),"vZ = ", self.getVitesse().projectionRef(refAvion).getZ())
        
        return torseurTot



#Utilisation:
# 1) Calculer et mettre a jour la vitesse et w du corps entier, avec les corpsRigides désactivé.
# 2) Set le DT de tous les corps rigides
# 3) Tant que tous les corps rigides ne sont pas "ok", recalculer et mettre a jour la vitesse et w
# 4) Reset les corps rigides
class CorpsRigide(Attachements):
    def __init__(self, position, father, referentielSol, epsilon, name = ""):
        super().__init__(position, 0, 0, father)
        self._name = name
        self._thisTurnTotalForce = 0
        self._thisTurnTotalForceX = 0
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
        deltaX = self.getPosition().projectionRef(self._referentielSol).x
        return 1/(1.0/self.father.getMasseTotal() + (deltaX**2)/self.father.getInertieTotal())

    def reset(self):
        self._thisTurnTotalForce = 0
        self._thisTurnTotalForceX = 0
        self._active = False

    def activer(self):
        self._active = True

    def _underground(self):
        return self.getPosition().changeRef(self._referentielSol).getZ()<=0

    def ok(self):
        if (not self._underground()) or (not self._active) or self.getVitesse().getZ()>0:
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
        vx = self.getVitesse().getX()
        Fr = 0
        if (abs(vx)>self._epsilon): #On applique les frottements
            if vx>0:
                Fr = -PM.muFrottementSol*F
            else:
                Fr = PM.muFrottementSol*F
        self._thisTurnTotalForce += F
        self._thisTurnTotalForceX += Fr
        return T.Torseur(self.getPosition(),E.Vecteur(Fr,F,self._referentielSol),0)
    
class Planeur():
    def __init__(self, world):
        self.world = world
        self.structure = Corps(T.Torseur(E.Vecteur(0,0,refAvion),E.Vecteur(0,0,refAvion),0), world, PM.masseTotal,PM.inertieTotal)   

        self.propulseur = Propulseur(E.Vecteur(PM.engine_x,PM.engine_z, refAvion),0,0,self.structure,0,PM.engineMaxThrust)
        self.structure.addAttachement(self.propulseur)

        #self.aileD = Aile(E.Vecteur(PM.ailesD_x_BA,PM.ailesD_z_BA,refAvion),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileD_S, PM.ailesD_corde, PM.flapsDPourcentageCordeArticulee,PM.flapsDPourcentageEnvergureArticulee, PM.flapsDMaxAngle, father = self.structure)
        self.aileD = Aile(E.Vecteur(PM.ailesD_x_BA,PM.ailesD_z_BA,refAvion),PolaireLineaire(PM.aileD_CzA, PM.aileD_Alpha_0, PM.aileD_Cx0, PM.aileD_k,0), PM.aileD_S, PM.ailesD_corde, PM.flapsDPourcentageCordeArticulee,PM.flapsDPourcentageEnvergureArticulee, PM.flapsDMaxAngle, world, father = self.structure)
        self.structure.addAttachement(self.aileD)

        #self.aileG = Aile(E.Vecteur(PM.ailesG_x_BA,PM.ailesG_z_BA,refAvion),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileG_S, PM.ailesG_corde, PM.flapsGPourcentageCordeArticulee,PM.flapsGPourcentageEnvergureArticulee, PM.flapsGMaxAngle, father = self.structure)
        self.aileG = Aile(E.Vecteur(PM.ailesG_x_BA,PM.ailesG_z_BA,refAvion),PolaireLineaire(PM.aileG_CzA, PM.aileG_Alpha_0, PM.aileG_Cx0, PM.aileG_k,0), PM.aileG_S, PM.ailesG_corde, PM.flapsGPourcentageCordeArticulee,PM.flapsGPourcentageEnvergureArticulee, PM.flapsGMaxAngle, world, father = self.structure)
        self.structure.addAttachement(self.aileG)

        #self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_Foyer,PM.empennageD_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageD_S,PM.empennageD_CzA, PM.empennageD_Alpha_0, PM.empennageD_Cx0, PM.empennageD_k,0 ,PM.elevDMaxAnglePourcentage)
        self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_BA,PM.empennageD_z_BA,refAvion),PolaireLineaire(PM.empennageD_CzA, PM.empennageD_Alpha_0,PM.empennageD_Cx0, PM.empennageD_k,0),PM.empennageD_S,PM.empennageD_corde,PM.elevDPourcentageCordeArticulee,PM.elevDPourcentageEnvergureArticulee,PM.elevDMaxAngle, world,father= self.structure)
        self.structure.addAttachement(self.empennageD)

        #self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_Foyer,PM.empennageG_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageG_S,PM.empennageG_CzA, PM.empennageG_Alpha_0, PM.empennageG_Cx0, PM.empennageG_k,0 ,PM.elevGMaxAnglePourcentage)
        self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_BA,PM.empennageG_z_BA,refAvion),PolaireLineaire(PM.empennageG_CzA, PM.empennageG_Alpha_0,PM.empennageG_Cx0, PM.empennageG_k,0),PM.empennageG_S,PM.empennageG_corde,PM.elevGPourcentageCordeArticulee,PM.elevGPourcentageEnvergureArticulee,PM.elevGMaxAngle, world,father= self.structure)
        self.structure.addAttachement(self.empennageG)

        self.p1 = CorpsRigide(E.Vecteur(PM.p1_x,PM.p1_z,refAvion),self.structure,refTerrestre,PS.maxAcceptablePenetrationSpeed,"p1")
        self.structure.addCorpsRigide(self.p1)
        self.p2 = CorpsRigide(E.Vecteur(PM.p2_x,PM.p2_z,refAvion),self.structure,refTerrestre,PS.maxAcceptablePenetrationSpeed,"p2")
        self.structure.addCorpsRigide(self.p2)
        self.p3 = CorpsRigide(E.Vecteur(PM.p3_x,PM.p3_z,refAvion),self.structure,refTerrestre,PS.maxAcceptablePenetrationSpeed,"p3")
        self.structure.addCorpsRigide(self.p3)
        self.p4 = CorpsRigide(E.Vecteur(PM.p4_x,PM.p4_z,refAvion),self.structure,refTerrestre,PS.maxAcceptablePenetrationSpeed,"p4")
        self.structure.addCorpsRigide(self.p4)
        self.p5 = CorpsRigide(E.Vecteur(PM.p5_x,PM.p5_z,refAvion),self.structure,refTerrestre,PS.maxAcceptablePenetrationSpeed,"p5")
        self.structure.addCorpsRigide(self.p5)

    def diffuseDictRawInput(self,rawInputDict):
        self.propulseur.setThrottlePercent(rawInputDict["throttle"])
        self.aileD.setBraquageFlaps(rawInputDict["flapsD"])
        self.aileG.setBraquageFlaps(rawInputDict["flapsG"])
        self.empennageD.setBraquageGouverne(rawInputDict["elevD"])
        self.empennageG.setBraquageGouverne(rawInputDict["elevG"])

    ##/!\ origine de l'avion dans l'interface prise au bati moteur
    def getPosition(self):
        return (self.structure.torseurCinematique.vecteur.ref.getOrigine() + self.propulseur.position.projectionRef(refTerrestre))

    def setPosition(self, newPosition):
        self.structure.torseurCinematique.vecteur.ref.setOrigine(newPosition.changeRef(refTerrestre))
        refAero.setOrigine(newPosition)
    
    def getAssiette(self):
        return normalize(self.structure.getTorseurCinematique().vecteur.ref.getAngleAxeY())

    def setAssiette(self, newAssiete):
        self.structure.getTorseurCinematique().vecteur.ref.setAngleAxeY(newAssiete)
        refAero.setAngleAxeY(self.structure.getTorseurCinematique().resultante.projectionRef(refTerrestre).arg())
    
    def getVitesse(self): 
        return self.propulseur.getVitesse()
    
    def setVitesse(self, newVitesse):
        self.structure.torseurCinematique.setResultante(newVitesse.projectionRef(refTerrestre))

    def getVitesseRot(self):
        return self.structure.getTorseurCinematique().moment
    
    def setVitesseRot(self, newVitesseRot):
        self.structure.getTorseurCinematique().setMoment(newVitesseRot)

    def generateRapportCollision(self):
        return self.structure.generateRapportCollision()

        


    


       
    