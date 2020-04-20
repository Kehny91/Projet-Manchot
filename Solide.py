import Espace as E
import Torseur as T
import numpy as np
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM
from Parametres import ParametresSimulation as PS
import Parametres as P
from DataTypes import RapportDeCollision
from DataManagement import normalize



refSol = E.Referentiel("refSol",0,E.Vecteur(0,0,E.ReferentielAbsolu())) 


class Corps(E.Referentiel):
    """Permet de definir le corps du drone, il s'agit d'un objet referentiel.
    \nle torseur cinematique est donnee au centre de gravite
    \n attribute E.Referentiel : refSol, le referentiel sol
    \n attribute T.TorseurCinematique : torseurCinematique, determine la vitesse de translation ainsi que la vitesse de rotation au centre de gravite
    \n attribute World : world, environnement du drone (vent)
    \n attribute float :  masse, masse de la structure 
    \n attribute float :  inertie, inertie du solide sur l'axe Y au centre de gravite
    \n attribute list : attachement, liste de solides relies a ce corps
    \n attribute list : corpsRigides, liste des corps rigides relies a ce corps
    """
    #Init
    def __init__(self, refSol, posCG, assiette, vitesseCG, w, world, masse = 0, inertie = 0):
        super().__init__("refCorps",assiette,posCG)
        self.refSol = refSol
        self.torseurCinematique = T.TorseurCinematique(E.Vecteur(0,0,self),w,vitesseCG)
        self.world = world
        self.masse = masse
        self.inertie = inertie
        self.father = None
        self.attachements = []
        self.corpsRigides = [] #ATTENTION, UN CORPS RIGIDE DOIT ETRE DANS LES DEUX LISTES
    
    #Geter/Seter
    def getPositionCG(self):
        """Renvoie la position du centre de gravite dans le refSol"""
        return self.getOrigine().changeRef(refSol)

    def setPositionCG(self, newPosition):
        """Modifie la position du centre de gravite dans le refSol"""
        self.setOrigine(newPosition.changeRef(self.refSol))
    
    def getAssiette(self):
        """Renvoie l angle du corps"""
        return self.getAngleAxeY()
    
    def setAssiette(self, newAssiette):
        """Modifie l assiette du corps"""
        self.setAngleAxeY(newAssiette)
    
    def getVitesseCG(self):
        """Renvoie la vitesse du CG dans le refCorps"""
        return self.torseurCinematique.getVitesse()
    
    def setVitesseCG(self, newVitesse):
        """Modifie la vitesse du CG dans le refCorps"""
        self.torseurCinematique.setVitesse(newVitesse)
    
    def getW(self):
        """Renvoie la vitesse de rotation du corps"""
        return self.torseurCinematique.getW()

    def setW(self, newW):
        """Modifie la vitesse de rotation du corps"""
        self.torseurCinematique.setW(newW)
    
    def getTorseurCinematique(self):
        """Renvoie le torseur cinematique applique au CG dans le refCorps"""
        return self.torseurCinematique

    #def setTorseurCinematique(self,newTorseurCinematique):
    #    """Modifie le torseur cinematique applique au CG dans le refCorps"""
    #    self.torseurCinematique = newTorseurCinematique.changeRef(self.refSol)
    
    def getMasse(self):
        return self.masse

    def setMasse(self,newMasse):
        self.masse=newMasse
    
    def getInertie(self):
        return self.inertie

    def setInertie(self,newInertie):
        self.masse=newInertie

    #Methodes
    def addAttachement(self,solide):
        """Rajoute un element au corps"""
        self.attachements.append(solide)
        solide.father = self

    def addCorpsRigide(self, cr):
        """Rajoute un corps rigide au corps principal"""
        self.addAttachement(cr)
        self.corpsRigides.append(cr)

    def deactivateAllCorpsRigide(self):
        """Desactive l'action de l'ensemble des corps rigides"""
        for cr in self.corpsRigides:
            cr.reset()

    def activateAllCorpsRigides(self, dt):
        """Active l'action de l'ensemble des corps rigides"""
        for cr in self.corpsRigides: 
            cr.activer()
            cr.setDt(dt)
    
    def corpsRigideOk(self):
        """Detecte si un corps solide actif est en contact du sol"""
        for cr in self.corpsRigides:
            if not cr.ok():
                return False
        return True
    
    def generateRapportCollision(self):
        """transmet les informations des collision sol au datatype"""
        out = RapportDeCollision()
        for cr in self.corpsRigides:
            if cr._thisTurnTotalForce > 0:
                out.addImpact(cr.position.changeRef(self.refSol),E.Vecteur(cr._thisTurnTotalForceX,cr._thisTurnTotalForce,self.refSol))
        return out

    def getTorseurPoids(self):
        """Renvoie le torseur poids applique en CG dans le refCorps"""
        return T.TorseurEffort(self.torseurCinematique.getPointAppl(),E.Vecteur(0,-self.masse * CE.g_0,self.refSol),0)

    def computeTorseurEfforts(self):
        """Renvoie un torseur des efforts exerces sur le corps et ses attachements
            \napplique au CG dans le refCorps"""
        torseurEfforts = self.getTorseurPoids()
        if (PS.printForces):
            print("Poids = ", torseurEfforts)
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement()
            if (PS.printForces):
                print(type(attachement),torseurEffortsAttachements)           
            torseurEfforts += torseurEffortsAttachements
        return torseurEfforts 
    
    def applyAction(self, torseurEfforts, totMass, totInertie, dt):
        """ Modifie le torseur cinematique sous l effet des efforts"""
        self.setVitesseCG(self.getVitesseCG() + torseurEfforts.getForce()*(dt/totMass))
        self.setW(self.getW() + torseurEfforts.getMoment()*(dt/totInertie))

    def updatePosAndAssiette(self,dt):
        """Modifie la position et l angle du corps en fonction de son torseur cinematique"""
        self.setPositionCG(self.getPositionCG() + self.getVitesseCG().projectionRef(self.refSol)*dt)
        self.setAssiette(self.getAssiette() + self.getW()*dt)

    def update(self,dt):
        """Actualise la cinematique du corps"""
        self.deactivateAllCorpsRigide()
        torseurEfforts = self.computeTorseurEfforts()
        self.applyAction(torseurEfforts, self.getMasse(), self.getInertie(), dt)
        self.activateAllCorpsRigides(dt)
        i=0
        while (not self.corpsRigideOk()):
            torseurEffortsCollisions = T.TorseurEffort(self.torseurCinematique.getPointAppl())
            for cr in self.corpsRigides:
                torseur = cr.getTorseurEffortsAttachement()
                torseurEffortsCollisions += torseur.changePoint(self.torseurCinematique.getPointAppl())
            self.applyAction(torseurEffortsCollisions, self.getMasse(), self.getInertie(), dt)
            i+=1
            if (i==100):
                assert False
        self.updatePosAndAssiette(dt)
 
class Attachements:
    """Permet de definir un attachament, c'est a dire un solide attachage a un corps
    \n attribute E.Vecteur : position, position du solide dans le ref du pere (ici corps)
    \n attribute Corps : father, corps sur lequel le solide est attache (ici corps)
    """
    #Init
    def __init__(self,position,father):
        self.position = position
        self.father = father

    #Geter/Seter
    def getPosition(self):
        """return la position de l attachament dans le refAvion"""
        return self.position

    def getVitesse(self):
        """return la vitesse de l attachament dans le refSol"""
        return self.father.getTorseurCinematique().changePoint(self.getPosition()).getVitesse().projectionRef(self.father.refSol)  

class Propulseur(Attachements):
    """Permet de definir un propulseur, c est un attachement.
    \n Cet attachement simule une force developee par un moteur et une helice
    \n attribute float : throttle, poussee consigne (en N)
    \n attribute float: throttleMax, poussee a puissance maximale (en N) 
    """
    #Init
    def __init__(self, position , father , throttle, throttleMax):
        super().__init__(position, father)
        self.throttle = throttle
        self.throttleMax = throttleMax
    
    #methode
    def setThrottlePercent(self, throttlePercent):
        """Modifie la poussee consigne"""
        self.throttle = self.throttleMax*throttlePercent
    
    #TODO :  montee en puissance du moteur
    def getTorseurEffortsAttachement(self):
        """Renvoie le torseur effort genere par le propulseur applique a la postion du bati moteur dans le refAvion"""
        torseurPoussee = T.TorseurEffort(self.position,E.Vecteur(self.throttle,0,self.father),0)
        return torseurPoussee

class SurfacePortante(Attachements):
    """Permet de definir une Surfaceportante, c est un attachement.
    \n Cet attachement simule les forces aero developees une surface dans un fluide en mouvement
    \n attribute float: S, surface portante/ailaire
    \n attribute Polaire : polaire, calcul de Cz et Cx en fonction de V et l'incidence
    \n attribute float :  corde, corde moyenne de la surface 
    """
    #Init
    def __init__(self, position, polaire, S, corde, father = None):
        super().__init__(position, father)
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
        moment = Fdyn*self.polaire.getCm(alpha,v)*self.corde
        forceAero = (VecteurXaeroLocal*(-1*drag) + VecteurZaeroLocal*lift).projectionRef(self.father)

        return T.TorseurEffort(self.position.changeRef(self.father),forceAero,moment)
        

    def getAlpha(self, VrefSol):
        """Renvoie l incidence de la surface portante"""
        return normalize(VrefSol.projectionRef(self.father).arg())

class Aile(SurfacePortante):
    """Permet de definir une aile, c est une surface portante.
    \n Cet attachement simule les forces aero developees par une aile
    \n attribute float : angleFlaps, angle consigne du flaps (en Rad)
    \n attribute float : angleMaxFlaps, angle maximal du flap (en Rad)
    \n attribute float : pourcentageCordeArticulee, pourcentage de la corde de l aile qui s articule (corde_flap/corde_aile) 
    \n attribute float : pourcentageEnvergureArticulee, pourcentage de l envergure de l aile qui s articule (envergure_flap/envergure_aile)
    \n attribute World : world, environnement de l aile  
    """
    #Init
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxFlaps, world, father = None):
        super().__init__(position, polaire , S, corde, father)
        self.angleFlaps = 0
        self.angleMaxFlaps = angleMaxFlaps
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.world = world
    
    #Metodes
    def setBraquageFlaps(self, pourcentageBraquageFlaps):
        """Modifie l angle flap consigne"""
        self.angleFlaps = pourcentageBraquageFlaps*self.angleMaxFlaps

    def getAlpha(self, VrefSol):
        """Renvoie une incidence theorique qui prend en compte l angle du flap"""
        alphaFixe = super().getAlpha(VrefSol) #Appelle SurfacePortante.getAlpha()
        theta = self.angleFlaps
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = np.arctan2(np.sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + np.cos(theta))
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        """Renvoie le torseur effort genere par l aile applique a la postion du bord d attaque dans le refAvion"""
        vLoc = self.getVitesse() - self.world.getVent(self.getPosition().changeRef(self.father.refSol))
        (alphaFixe,gainAlpha) = self.getAlpha(vLoc)
        torseurFixe = self.getResultanteAero(alphaFixe, vLoc)*(1 - self.pourcentageEnvergureArticulee)
        torseurFlaps = self.getResultanteAero(normalize(alphaFixe + gainAlpha),vLoc)*self.pourcentageEnvergureArticulee
        torseurTot = torseurFixe + torseurFlaps
        return torseurTot


class Empennage(SurfacePortante):
    """Permet de definir un empennage, c est une surface portante.
    \n Cet attachement simule les forces aero developees par un empennage
    \n attribute float : angleGouverne, angle consigne de la gouverne (en Rad)
    \n attribute float : angleMaxGouverne, angle maximal de la gouverne (en Rad)
    \n attribute float : pourcentageCordeArticulee, pourcentage de la corde de l empennage qui s articule (corde_gouverne/corde_flap) 
    \n attribute float : pourcentageEnvergureArticulee, pourcentage de l envergure de l aile qui s articule (envergure_gouverne/envergure_flap)
    \n attribute World : world, environnement de l aile  
    """
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxGouverne, world, father = None):
        super().__init__(position, polaire , S, corde, father)
        self.angleGouverne = 0
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.angleMaxGouverne = angleMaxGouverne
        self.world = world
    
    def setBraquageGouverne(self, pourcentageBraquageGouverne):
        """Modifie l angle gouverne consigne"""
        self.angleGouverne = pourcentageBraquageGouverne*self.angleMaxGouverne

    def getAlpha(self, VrefSol):
        """Renvoie une incidence theorique qui prend en compte l angle de la gouverne"""
        alphaFixe = super().getAlpha(VrefSol) #Appelle SurfacePortante.getAlpha()
        theta = self.angleGouverne
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = np.arctan2(np.sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + np.cos(theta))
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        """Renvoie le torseur effort genere par l empennage applique a la postion du bord d attaque dans le refAvion"""
        vLoc = self.getVitesse() - self.world.getVent(self.getPosition().changeRef(self.father.refSol))
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
    #TODO alex, developer la doc
    """Permet de definir un corps rigide, il s agit d attachements qui ne peuvent pas penetrer dans le sol
    \n attribute String : name, nom du corps rigide
    \n attribute 

    """
    #Init
    def __init__(self, position, father, epsilon, name = ""):
        super().__init__(position, father)
        self._name = name
        self._thisTurnTotalForce = 0
        self._thisTurnTotalForceX = 0
        self._epsilon = epsilon
        self._referentielSol = self.father.refSol
        self._axeXSol = self.father.refSol.getAxeX()
        self._axeZSol = self.father.refSol.getAxeZ()
        self._dt = 0.001
        self._active = False

    def setDt(self,dt):
        self._dt = dt

    def _m0(self):
        #deltaX est censé etre la distance CG -> self, projetée sur l'axe X du sol !
        deltaX = self.getPosition().projectionRef(self._referentielSol).x
        return 1/(1.0/self.father.getMasse() + (deltaX**2)/self.father.getInertie())

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
            return T.TorseurEffort(self.getPosition())
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
        return T.TorseurEffort(self.getPosition(),E.Vecteur(Fr,F,self._referentielSol),0)
    



    


       
    