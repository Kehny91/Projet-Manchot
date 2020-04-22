import Physique.Espace as E
import Physique.Torseur as T
import Physique.SystemeMeca as Sy1O
from math import pi,atan2,cos,sin
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM
from Parametres import ParametresSimulation as PS
from Data.DataTypes import RapportDeCollision
from Data.DataManagement import normalize 


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
        #Attention, la vitesse etant defini par rapport a ce referentiel, il ne faut pas qu'elle tourne avec
        backupV = self.torseurCinematique.getVitesse().projectionRef(self.refSol)
        self.setAngleAxeY(newAssiette)
        self.torseurCinematique.setVitesse(backupV)
    
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
    
    def getMasse(self):
        return self.masse

    def setMasse(self,newMasse):
        self.masse=newMasse
    
    def getInertie(self):
        return self.inertie

    def setInertie(self,newInertie):
        self.masse=newInertie

    #Methodes liees aux attachements et corps rigides
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
            if cr._thisTurnTotalForceN > 0:
                out.addImpact(cr.position.changeRef(self.refSol), cr.getThisTurnTotalForce())
        return out

    #methodes liees a la mise en equation du solide
    def getTorseurPoids(self):
        """Renvoie le torseur poids applique en CG dans le refCorps"""
        return T.TorseurEffort(self.torseurCinematique.getPointAppl(),E.Vecteur(0,-self.masse * CE.g_0,self.refSol),0)

    def computeTorseurEfforts(self):
        """Renvoie un torseur des efforts exerces sur le corps et ses attachements
            \napplique au CG dans le refCorps"""
        torseurEfforts = self.getTorseurPoids()
        if (PS.printForces):
            print("Poids = ", torseurEfforts.debug())
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement()
            if (PS.printForces):
                print(type(attachement),torseurEffortsAttachements.debug())    
                print(type(attachement),torseurEffortsAttachements.changePoint(torseurEfforts.pointAppl).debug()) 
            torseurEfforts += torseurEffortsAttachements
        if (PS.printForces):
            print("total ", torseurEfforts.debug())
        return torseurEfforts 
    
    def updateCinematique(self, torseurEfforts, totMass, totInertie, dt):
        """ Modifie le torseur cinematique sous l effet des efforts"""
        if (PS.printDebugCinetique):
            print("vitesse CG avant ", self.getVitesseCG().projectionRef(self).debug())
            print("w avant ", self.getW())
        self.setVitesseCG(self.getVitesseCG() + torseurEfforts.getForce()*(dt/totMass))
        self.setW(self.getW() + torseurEfforts.getMoment()*(dt/totInertie))
        if (PS.printDebugCinetique):
            print("vitesse CG apres ", self.getVitesseCG().projectionRef(self).debug())
            print("apres avant ", self.getW())

    def updatePosAndAssiette(self,dt):
        """Modifie la position et l angle du corps en fonction de son torseur cinematique"""
        self.setPositionCG(self.getPositionCG() + self.getVitesseCG().projectionRef(self.refSol)*dt)
        self.setAssiette(self.getAssiette() + self.getW()*dt)

    def update(self,dt):
        """Actualise la cinematique du corps"""
        self.deactivateAllCorpsRigide()
        torseurEfforts = self.computeTorseurEfforts()
        self.updateCinematique(torseurEfforts, self.getMasse(), self.getInertie(), dt)
        self.activateAllCorpsRigides(dt)
        i=0
        while (not self.corpsRigideOk()):
            for cr in self.corpsRigides:
                torseur = cr.getTorseurEffortsAttachement()
                self.updateCinematique(torseur.changePoint(self.torseurCinematique.getPointAppl()), self.getMasse(), self.getInertie(), dt)
            i+=1
            if (i==1000):
                assert False, "ERROR ERROR ERROR Les collisions n'ont pas pu etre resolues"

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
    \n attribute float: puissanceMax, puissance maximale du propulseur
    \n attribute Systeme1Ordre: tau, temps de reaction du propulseur  
    """
    #Init
    def __init__(self, position , father , throttle, throttleMax, puissanceMax, pousseeReelle):
        super().__init__(position, father)
        self.throttle = throttle
        self.throttleMax = throttleMax
        self.puissanceMax = puissanceMax
        self.pousseeReelle = pousseeReelle
    
    #methode
    def setThrottlePercent(self, throttlePercent):
        """Modifie la poussee consigne"""
        self.throttle = self.throttleMax*throttlePercent
    
    def getThrustConsigne(self):
        """Renvoie la poussee consigne"""
        # Un moteur a hélice développe une puissance P=V*T constante, pas une poussée constante.
        # Cependant si v==0 et notre moteur developpe 505W, on a T = P / V = 505 / 0
        # Cette regle ne s'applique pas aux basses vitesse car il faudrait prendre en compte la vitesse de l'air mise en mouvement par l'hélice
        # Ainsi, au basses vitesses, on considérera une poussée constante, au hautes vitesse, une puissance constante
        V = self.getVitesse().norm()
        if (V<1):
            return self.throttle
        else:
            return min(self.throttle,self.throttle*self.puissanceMax/(V*self.throttleMax))

    def getTorseurEffortsAttachement(self):
        """Renvoie le torseur effort genere par le propulseur applique a la postion du bati moteur dans le refAvion"""
        self.pousseeReelle.setConsigne(self.getThrustConsigne())
        torseurPoussee = T.TorseurEffort(self.position,E.Vecteur(self.pousseeReelle.getValue(),0,self.father),0)
        return torseurPoussee

class SurfacePortante(Attachements):
    """Permet de definir une Surfaceportante, c est un attachement.
    \n Cet attachement simule les forces aero developees une surface dans un fluide en mouvement
    \n attribute float: S, surface portante/ailaire
    \n attribute Polaire : polaire, calcul de Cz et Cx en fonction de V et l'incidence
    \n attribute float :  corde, corde moyenne de la surface 
    """
    #Init
    def __init__(self, position, polaire, S, corde, angleCalage, father = None):
        super().__init__(position, father)
        self.S = S
        self.polaire = polaire
        self.corde = corde
        self.angleCalage = angleCalage
    
    def getResultanteAero(self, alpha, VrefSol):
        """Renvoie le torseur des forces appliquees au bord d attaque dans le refCorps"""
        VecteurXaeroLocal = VrefSol.unitaire()
        VecteurZaeroLocal = VecteurXaeroLocal.rotate(-pi/2)  
        v = VrefSol.norm()
        Fdyn = 0.5 * CE.rho_air_0 *self.S*(v**2)
        lift = Fdyn*self.polaire.getCl(alpha,v)
        drag = Fdyn*self.polaire.getCd(alpha,v)
        moment = Fdyn*self.polaire.getCm(alpha,v)*self.corde
        forceAero = (VecteurXaeroLocal*(-1*drag) + VecteurZaeroLocal*lift).projectionRef(self.father)
        return T.TorseurEffort(self.position.changeRef(self.father),forceAero,moment)
        

    def getAlpha(self, V):
        """Renvoie l incidence de la surface portante"""
        return normalize(V.projectionRef(self.father).arg()) + self.angleCalage

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
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxFlaps, angleCalage, world, father = None):
        super().__init__(position, polaire , S, corde, angleCalage, father)
        self.angleFlaps = 0
        self.angleMaxFlaps = angleMaxFlaps
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.world = world
    
    #Metodes
    def setBraquageFlaps(self, pourcentageBraquageFlaps):
        """Modifie l angle flap consigne"""
        self.angleFlaps = pourcentageBraquageFlaps*self.angleMaxFlaps

    def getAlpha(self, V):
        """Renvoie une incidence theorique qui prend en compte l angle du flap"""
        alphaFixe = super().getAlpha(V) #Appelle SurfacePortante.getAlpha()
        theta = self.angleFlaps
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = atan2(sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + cos(theta))
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
    def __init__(self, position, polaire, S, corde, pourcentageCordeArticulee, pourcentageEnvergureArticulee, angleMaxGouverne, angleDemiDiedre, angleCalage, world, father = None):
        super().__init__(position, polaire , S, corde, angleCalage, father)
        self.angleGouverne = 0
        self.pourcentageCordeArticulee = pourcentageCordeArticulee
        self.pourcentageEnvergureArticulee = pourcentageEnvergureArticulee
        self.angleMaxGouverne = angleMaxGouverne
        self.angleDemiDiedre = angleDemiDiedre
        self.world = world
    
    def setBraquageGouverne(self, pourcentageBraquageGouverne):
        """Modifie l angle gouverne consigne"""
        self.angleGouverne = pourcentageBraquageGouverne*self.angleMaxGouverne

    def getAlpha(self, V):
        """Renvoie une incidence theorique qui prend en compte l angle de la gouverne"""
        alphaFixe = super().getAlpha(V) #Appelle SurfacePortante.getAlpha()
        theta = self.angleGouverne
        if self.pourcentageCordeArticulee == 0:
            gainAlpha = 0
        else:
            gainAlpha = (atan2(sin(theta),(1-self.pourcentageCordeArticulee)/self.pourcentageCordeArticulee + cos(theta)))*cos(self.angleDemiDiedre)
        return  (normalize(alphaFixe) , normalize(gainAlpha))
        
    def getTorseurEffortsAttachement(self):
        """Renvoie le torseur effort genere par l empennage applique a la postion du bord d attaque dans le refAvion"""
        vLoc = (self.getVitesse() - self.world.getVent(self.getPosition().changeRef(self.father.refSol))).projectionRef(self.father)
        vLoc.z = vLoc.z*cos(self.angleDemiDiedre) #Correction du z efficace!

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
    """Permet de definir un corps rigide, il s agit d attachements qui ne peuvent pas penetrer dans le sol
    \n attribute String : name, nom du corps rigide
    \n attribute 

    """
    #Init
    def __init__(self, position, father, epsilon, world, name = ""):
        super().__init__(position, father)
        self._name = name
        self._world = world
        self._thisTurnTotalForceN = 0
        self._thisTurnTotalForceT = 0
        self._T = None
        self._N = None
        self._m0opti = None
        self._vpnOpti = None
        self._epsilon = epsilon
        self._referentielSol = self.father.refSol
        self._dt = 0.001
        self._active = False
        self._statique = True

    def setDt(self,dt):
        self._dt = dt

    def _m0(self, normale):
        deltaX2 = self.getPosition().projectionRef(self._referentielSol).x**2
        deltaZ2 = self.getPosition().projectionRef(self._referentielSol).z**2
        OPn2    = self.getPosition().projectionRef(self._referentielSol).prodScal(normale)**2
        return 1/(1.0/self.father.getMasse() + (deltaX2 + deltaZ2 - OPn2)/self.father.getInertie())

    def reset(self):
        self._thisTurnTotalForceN = 0
        self._thisTurnTotalForceT = 0
        self._statique = True
        self._active = False
        self._T = None
        self._N = None
        self._m0optiN = None
        self._targetVN = None

    def activer(self):
        self._active = True


    def ok(self):
        
        if not self._world.isInSomething(self.position.changeRef(self._referentielSol)) or (not self._active):
            #Si on est pas dans un obstacle  ou desactivé
            return True #Ok

        if (self._N == None):
            self._N = self._world.getNormaleObstacle(self.position.changeRef(self._referentielSol))

        vpn = self.getVitesse().prodScal(self._N)

        #print(self._name, " targetVn ", self._targetVN, " vn ", vpn)

        if (self._thisTurnTotalForceN==0 and vpn>0):
            #Si de toute facon, on s'en allait:
            return True

        if (self._m0optiN == None):
                self._m0optiN = self._m0(self._N)

        if (self._targetVN == None):
            #Si je n'ai pas de target
            if (vpn*self._m0optiN<-1):
                #Si le choc est violent (1kg a 1ms)
                self._targetVN = -1*PM.resitution*vpn
            else:
                self._targetVN = 0
        
        if(self._T == None):
            self._T = self._N.rotate(pi/2)

        if (self._statique):
            return abs(self.getVitesse().prodScal(self._T))<self._epsilon and abs(vpn - self._targetVN)<self._epsilon
        else:
            return abs(vpn - self._targetVN)<self._epsilon

    def getTorseurEffortsAttachement(self):
        """Le dt doit etre celui qui sera utilisé pour l'intégration de la vitesse"""
        if (self.ok()):
            return T.TorseurEffort(self.getPosition())
        #Sinon
        if (self._N == None):
            self._N = self._world.getNormaleObstacle(self.position.changeRef(self._referentielSol))
        if (self._T == None):
            self._T = self._N.rotate(pi/2)
        if (self._m0optiN == None):
            self._m0optiN = self._m0(self._N)
        vpn = self.getVitesse().prodScal(self._N)
        vpt = self.getVitesse().prodScal(self._T)

        Fn = (self._targetVN - vpn)*self._m0optiN/self._dt
        #La forceNormale totale appliquée ne peut pas etre négative, donc au minimum, F peut valoir -thisTurnTotalForce
        Fn = max(-1*self._thisTurnTotalForceN,Fn)
        self._thisTurnTotalForceN += Fn

        Ft = -1*vpt*self._m0(self._T)/self._dt
        #La force tangentielle ne peut pas etre plus grande que muFn
        current = self._thisTurnTotalForceT
        self._thisTurnTotalForceT = self._thisTurnTotalForceT + Ft
        if self._thisTurnTotalForceT <= -self._thisTurnTotalForceN*PM.muFrottement:
            self._thisTurnTotalForceT = -self._thisTurnTotalForceN*PM.muFrottement
            self._statique = False
        elif self._thisTurnTotalForceT >= self._thisTurnTotalForceN*PM.muFrottement:
            self._thisTurnTotalForceT = self._thisTurnTotalForceN*PM.muFrottement
            self._statique = False
        else:
            self._statique = True

        Ft = self._thisTurnTotalForceT - current
        
        return T.TorseurEffort(self.getPosition(),self._N*Fn + self._T*Ft,0)

    def getThisTurnTotalForce(self):
        return (self._N*self._thisTurnTotalForceN + self._T*self._thisTurnTotalForceT).projectionRef(self._referentielSol)