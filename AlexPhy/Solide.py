import AlexPhy.Espace as E
import AlexPhy.Torseur as T
import numpy as np
from Polaire import PolaireLineaire,PolaireTabulee
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM
import Parametres as P
from DataManagement import normalize


refAbs = E.ReferentielAbsolu()


class Corps(E.Referentiel): #Un corps est un referentiel
    """classe Corps
    permet de definir un le corps du planeur, le torseur cinematique est donnee au centre de gravite
    \n attribute T.Torseur : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation au centre de gravite
    \n attribute float :  masse, masse de la structure 
    \n attribute float :  inertie, inertie du solide sur l'axe Y au centre de gravite
    \n attribute list : attachement, liste de solides relies a ce corps
    """
    #Init
    def __init__(self, referentielSol, posCG, vitesseCG, angleRefY, w, masse, inertie):
        super().__init__("refCorps", angleRefY, posCG)
        self.referentielSol = referentielSol
        self.torseurCinematique = T.TorseurCinematique(E.Vecteur(0,0,self), w, vitesseCG) #J'ecris le torseur a mon orgine (CG)
        self.masse = masse
        self.inertie = inertie
        self.father = None
        self.attachements = []
        self.corpsRigides = [] #ATTENTION, UN CORPS RIGIDE DOIT ETRE DANS LES DEUX LISTES
    
    def setPosCG(self, pos):
        self.setOrigine(pos)

    def getPosCG(self):
        return self.getOrigine()

    def getV(self):
        return self.torseurCinematique.getVitesse()
    
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
            vecteurVersAtt = p.position.changeRef(self)
            inertietot += p.inertie + p.masse* (vecteurVersAtt.x**2 + vecteurVersAtt.z**2)
        return inertietot

    def addAttachement(self,solide):
        self.attachements.append(solide)
        solide.father = self

    def addCorpsRigide(self, cr):
        self.addAttachement(cr)
        self.corpsRigides.append(cr)
    
    def update(self,dt):
        torseurEfforts = self.computeTorseurEfforts().changePoint(self.getPosCG())
        self.torseurCinematique.applyAction(torseurEfforts,self.getMasseTotal(),self.getInertieTotal(),dt)
        self.updatePosAndAssiette(dt)

    def updatePosAndAssiette(self, dt):
        self.setPosCG( self.getPosCG() + self.torseurCinematique.getVitesse()*dt )
        self.setAngleAxeY( self.getAngleAxeY() + self.torseurCinematique.getW()*dt )

    def computeTorseurEfforts(self):
        torseurEfforts = self.getTorseurPoids().changePoint(self.getPosCG())
        print("")
        print("Poids = ", torseurEfforts)
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement()
            print(type(attachement),torseurEffortsAttachements)          
            torseurEfforts += torseurEffortsAttachements
        print("")
        return torseurEfforts 
 
    def getTorseurPoids(self):
        return T.TorseurAction(self.getPosCG().changeRef(self),E.Vecteur(0,-self.masse * CE.g_0,self.referentielSol),0)


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
        return self.father.torseurCinematique.changePoint(self.position).getVitesse()

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
        return T.TorseurAction(self.position,E.Vecteur(self.throttle,0,self.father),0)

class SurfacePortante(Attachements):
    def __init__(self, position, polaire, S, corde, masse = 0, inertie = 0, father = None):
        super().__init__(position , masse, inertie, father)
        self.S = S
        self.polaire = polaire
        self.corde = corde
    
    def getResultanteAero(self,alpha): #Permet de ne pas creer puis sommer les torseur
        V = self.getVitesse()
        VecteurXaeroLocal = V.unitaire()
        print("X",VecteurXaeroLocal)
        VecteurZaeroLocal = VecteurXaeroLocal.rotate(-np.pi/2)
        print("Z",VecteurZaeroLocal)
        
        v = V.norm()
        Fdyn = 0.5 * CE.rho_air_0 *self.S*(v**2)
        lift = Fdyn*self.polaire.getCl(alpha,v)
        drag = Fdyn*self.polaire.getCd(alpha,v)
        print("drag ",drag)
        moment = Fdyn*self.polaire.getCm(alpha,v)*self.corde

        forceAero = (VecteurXaeroLocal*(-1*drag) + VecteurZaeroLocal*lift).projectionRef(self.father)
        return T.TorseurAction(self.position, forceAero, moment)

    #TODO Tom. Attention, alpha c'est bien une différence d'angle entre l'angle du fuselage et l'angle de la vitesse
    def getAlpha(self, V):
        #print("Assiette = ",refAvion.getAngleAxeY())
        return normalize(V.projectionRef(self.father).arg())


class Aile(SurfacePortante):
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxFlaps, masse = 0, inertie = 0, father = None):
        super().__init__(position, polaire , S, corde, masse, inertie, father)
        self.angleFlaps = 0
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.angleMaxFlaps = angleMaxFlaps
    
    def setBraquageFlaps(self, pourcentageBraquageFlaps):
        self.angleFlaps = pourcentageBraquageFlaps*self.angleMaxFlaps

    def getAlpha(self):
        alphaFixe = super().getAlpha(self.getVitesse()) #Appelle SurfacePortante.getAlpha()
        theta = self.angleFlaps
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = np.arctan2(np.sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + np.cos(theta))
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        v = self.getVitesse().norm()
        (alphaFixe,gainAlpha) = self.getAlpha()
        torseurFixe = self.getResultanteAero(alphaFixe)*(1 - self.pourcentageEnvergureArticulee)
        torseurFlaps = self.getResultanteAero(normalize(alphaFixe + gainAlpha))*self.pourcentageEnvergureArticulee
        torseurTot = torseurFixe + torseurFlaps
        #print("aile v = ",v,"alpha = ", normalize(alphaFixe + gainAlpha)," fzAvion = ",torseurTot.getResultante().projectionRef(refAvion).getZ()," fxAvion = ", torseurTot.getResultante().projectionRef(refAvion).getX())
        return torseurTot


class Empennage(SurfacePortante):
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxGouverne, masse = 0, inertie = 0, father = None):
        super().__init__(position, polaire , S, corde, masse, inertie, father)
        self.angleGouverne = 0
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.angleMaxGouverne = angleMaxGouverne
    
    def setBraquageGouverne(self, pourcentageBraquageGouverne):
        self.angleGouverne = pourcentageBraquageGouverne*self.angleMaxGouverne

    def getAlpha(self):
        alphaFixe = super().getAlpha(self.getVitesse()) #Appelle SurfacePortante.getAlpha()
        theta = self.angleGouverne
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = np.arctan2(np.sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + np.cos(theta))
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        v = self.getVitesse().norm()
        (alphaFixe,gainAlpha) = self.getAlpha()
        torseurFixe = self.getResultanteAero(alphaFixe)*(1 - self.pourcentageEnvergureArticulee)
        torseurGouverne = self.getResultanteAero(normalize(alphaFixe + gainAlpha))*self.pourcentageEnvergureArticulee
        torseurTot = torseurFixe + torseurGouverne
        #print("emp v = ",v,"alpha = ", alphaFixe + gainAlpha," fzavion = ",torseurTot.getResultante().projectionRef(refAvion).getZ()," fxavion = ", torseurTot.getResultante().projectionRef(refAvion).getX(),"vZ = ", self.getVitesse().projectionRef(refAvion).getZ())
        
        return torseurTot



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
    
class Planeur():
    def __init__(self,referentielSol):
        self.referentielSol = referentielSol
        self.structure = Corps(referentielSol,E.Vecteur(0,0,referentielSol),E.Vecteur(0,0,referentielSol),0,0,PM.masseTotal,PM.inertieTotal) 

        self.propulseur = Propulseur(E.Vecteur(PM.engine_x,PM.engine_z, self.structure),0,0,self.structure,0,PM.engineMaxThrust)
        self.structure.addAttachement(self.propulseur)

        #self.aileD = Aile(E.Vecteur(PM.ailesD_x_BA,PM.ailesD_z_BA,refAvion),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileD_S, PM.ailesD_corde, PM.flapsDPourcentageCordeArticulee,PM.flapsDPourcentageEnvergureArticulee, PM.flapsDMaxAngle, father = self.structure)
        self.aileD = Aile(E.Vecteur(PM.ailesD_x_BA,PM.ailesD_z_BA,self.structure),PolaireLineaire(PM.aileD_CzA, PM.aileD_Alpha_0, PM.aileD_Cx0, PM.aileD_k,0), PM.aileD_S, PM.ailesD_corde, PM.flapsDPourcentageCordeArticulee,PM.flapsDPourcentageEnvergureArticulee, PM.flapsDMaxAngle, father = self.structure)
        self.structure.addAttachement(self.aileD)

        #self.aileG = Aile(E.Vecteur(PM.ailesG_x_BA,PM.ailesG_z_BA,refAvion),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileG_S, PM.ailesG_corde, PM.flapsGPourcentageCordeArticulee,PM.flapsGPourcentageEnvergureArticulee, PM.flapsGMaxAngle, father = self.structure)
        self.aileG = Aile(E.Vecteur(PM.ailesG_x_BA,PM.ailesG_z_BA,self.structure),PolaireLineaire(PM.aileG_CzA, PM.aileG_Alpha_0, PM.aileG_Cx0, PM.aileG_k,0), PM.aileG_S, PM.ailesG_corde, PM.flapsGPourcentageCordeArticulee,PM.flapsGPourcentageEnvergureArticulee, PM.flapsGMaxAngle, father = self.structure)
        self.structure.addAttachement(self.aileG)

        #self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_Foyer,PM.empennageD_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageD_S,PM.empennageD_CzA, PM.empennageD_Alpha_0, PM.empennageD_Cx0, PM.empennageD_k,0 ,PM.elevDMaxAnglePourcentage)
        self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_BA,PM.empennageD_z_BA,self.structure),PolaireLineaire(PM.empennageD_CzA, PM.empennageD_Alpha_0,PM.empennageD_Cx0, PM.empennageD_k,0),PM.empennageD_S,PM.empennageD_corde,PM.elevDPourcentageCordeArticulee,PM.elevDPourcentageEnvergureArticulee,PM.elevDMaxAngle,father= self.structure)
        self.structure.addAttachement(self.empennageD)

        #self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_Foyer,PM.empennageG_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageG_S,PM.empennageG_CzA, PM.empennageG_Alpha_0, PM.empennageG_Cx0, PM.empennageG_k,0 ,PM.elevGMaxAnglePourcentage)
        self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_BA,PM.empennageG_z_BA,self.structure),PolaireLineaire(PM.empennageG_CzA, PM.empennageG_Alpha_0,PM.empennageG_Cx0, PM.empennageG_k,0),PM.empennageG_S,PM.empennageG_corde,PM.elevGPourcentageCordeArticulee,PM.elevGPourcentageEnvergureArticulee,PM.elevGMaxAngle,father= self.structure)
        self.structure.addAttachement(self.empennageG)

    def diffuseDictRawInput(self,rawInputDict):
        pass
        #self.propulseur.setThrottlePercent(rawInputDict["throttle"])
        #self.aileD.setBraquageFlaps(rawInputDict["flapsD"])
        #self.aileG.setBraquageFlaps(rawInputDict["flapsG"])
        self.empennageD.setBraquageGouverne(rawInputDict["elevD"])
        self.empennageG.setBraquageGouverne(rawInputDict["elevG"])

    def getPositionCG(self):
        return self.structure.getPosCG()

    def getAssiette(self):
        return normalize(self.structure.getAngleAxeY())

    def getVitesseCG(self): 
       return self.structure.torseurCinematique.getVitesse()

    def getVitesseRot(self):
        return self.structure.torseurCinematique.getW()  

    def setPositionCG(self, newPosition):
        self.structure.setPosCG(newPosition)
    
    def setAssiette(self, newAssiete):
        self.structure.setAngleAxeY(newAssiete)
    
    def setVitesseCG(self, newVitesse):
        self.structure.torseurCinematique.setV(newVitesse)

    def setWCG(self, w):
        self.structure.torseurCinematique.setW(w)



    def getPositionBati(self):
        return self.propulseur.getPosition().changeRef(self.referentielSol)

    def getVitesseBati(self): 
       return self.propulseur.getVitesse().projectionRef(self.referentielSol)

    def setPositionBati(self, newPosition):
        self.setPositionCG(newPosition - self.propulseur.position.projectionRef(newPosition.getRef()))
    
    def setVitesseBati(self, newVitesse):
        tc = self.structure.torseurCinematique.changePoint(self.propulseur.position)
        tc.setV(newVitesse)
        tc = tc.changePoint(self.getPositionCG())
        self.setVitesseCG(tc.getVitesse())