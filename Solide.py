import Espace as E
import Torseur as T
import numpy as np
from Polaire import PolaireLineaire,PolaireTabulee
from Parametres import ConstanteEnvironement as CE
from Parametres import ParametresModele as PM
import Parametres as P



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
        torseurEfforts = self.computeTorseurEfforts().changePoint(self.torseurCinematique.vecteur) # C'est mieux de faire le PFD au CG...
        #PFD
        accX = torseurEfforts.resultante.x/self.getMasseTotal() #- self.torseurCinematique.moment*self.torseurCinematique.resultante.z
        accZ = torseurEfforts.resultante.z/self.getMasseTotal() #+ self.torseurCinematique.moment*self.torseurCinematique.resultante.x
        wpoint = torseurEfforts.moment/self.getInertieTotal()
        vecteurAcce = E.Vecteur(accX,accZ,refTerrestre)
        #construction vecteur acceleration
        torseurAcc= T.Torseur(self.torseurCinematique.vecteur,vecteurAcce.projectionRef(refAvion),wpoint)
        #update
        self.torseurCinematique = self.torseurCinematique + torseurAcc*dt
        self.move(self.torseurCinematique,dt)

    def move(self,torseurCinematique,dt):
        self.torseurCinematique.vecteur.ref.setOrigine(self.torseurCinematique.vecteur.ref.getOrigine() + torseurCinematique.resultante.projectionRef(refTerrestre)*dt)
        self.torseurCinematique.vecteur.ref.setAngleAxeY(self.torseurCinematique.vecteur.ref.getAngleAxeY() + torseurCinematique.moment*dt )
        #TODO Mettre a jour refaero ?

    def computeTorseurEfforts(self):
        print("Torseur computations")
        torseurEfforts = self.getTorseurPoids().changePoint(self.torseurCinematique.vecteur)
        print("Poids = ",torseurEfforts)
        print
        for attachement in self.attachements:
            torseurEffortsAttachements = attachement.getTorseurEffortsAttachement().changePoint(self.torseurCinematique.vecteur)
            torseurEfforts += torseurEffortsAttachements
            print("Attachement situé en ",attachement.position," = ", torseurEffortsAttachements)
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
        vitessez =  self.father.getTorseurCinematique().resultante.projectionRef(refTerrestre).z - self.father.getTorseurCinematique().moment * self.position.projectionRef(refTerrestre).x
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
        #torseurPoussee = T.Torseur(self.position,E.Vecteur(self.throttle,0,refAvion),0)
        #return torseurPoussee
        return T.Torseur(self.position,E.Vecteur(0,0,refAvion),0) #DEBUGUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUG

class SurfacePortante(Attachements):
    def __init__(self, position, polaire, S, corde, masse = 0, inertie = 0, father = None):
        super().__init__(position , masse, inertie, father)
        self.S = S
        self.polaire = polaire
        self.corde = corde

    def getResultanteAero(self, alpha, v): #Permet de ne pas creer puis sommer les torseur
        Fdyn = 0.5 * CE.rho_air_0 *self.S*(v**2)
        lift = Fdyn*self.polaire.getCl(alpha,v)
        drag = Fdyn*self.polaire.getCd(alpha,v)
        moment = Fdyn*self.polaire.getCm(alpha,v)*self.corde # IL FAUDRA CHECKER LES SIGNES !!!
        #return T.Torseur(self.position.changeRef(refAero),E.Vecteur(-drag,lift,refAero),moment)
        return T.Torseur(self.position.changeRef(refAvion),E.Vecteur(-drag,lift,refAvion),moment)

    #TODO Tom. Attention, alpha c'est bien une différence d'angle entre l'angle du fuselage et l'angle de la vitesse
    def getAlpha(self):
        vitesseRefSol = self.getVitesse()
        angleVitesse = vitesseRefSol.arg()
        refAero.setOrigine(refAvion.getOrigine()) # Ces 2 lignes
        refAero.setAngleAxeY(angleVitesse)        # vont etre appelé inutilment beaucoup trop de fois
        return vitesseRefSol.projectionRef(refAvion).arg() # TODO Tom, tu me confirmes que projectionRef change juste la base dans laquelle on mesure les coordonnées du vecteur ?



class Aile(SurfacePortante):
    def __init__(self, position, polaire, S, corde, pourcentageInfluenceFlaps, angleMaxFlaps, masse = 0, inertie = 0, father = None):
        super().__init__(position, polaire , S, corde, masse, inertie, father)
        self.angleFlaps = 0
        self.pourcentageInfluenceFlaps = pourcentageInfluenceFlaps
        self.angleMaxFlaps = angleMaxFlaps
    
    def setBraquageFlaps(self, pourcentageBraquageFlaps):
        self.angleFlaps = pourcentageBraquageFlaps*self.angleMaxFlaps

    def getAlpha(self):
        alphaFixe = super().getAlpha() #Appelle SurfacePortante.getAlpha()
        return  alphaFixe + 0*self.angleFlaps*self.pourcentageInfluenceFlaps #DEBUUUUUUUUUUUUUUG
        
    def getTorseurEffortsAttachement(self):
        v = self.getVitesse().norm()
        alpha = self.getAlpha()
        torseurTot = self.getResultanteAero(alpha,v)
        print("aile v = ",v,"alpha = ", alpha," fzAvion = ",torseurTot.getResultante().projectionRef(refAvion).getZ()," fxAvion = ", torseurTot.getResultante().projectionRef(refAvion).getX())
        return torseurTot


class Empennage(SurfacePortante):
    def __init__(self, position, polaire, S, corde, pourcentageInfluenceGouverne, angleMaxGouverne, masse = 0, inertie = 0, father = None):
        super().__init__(position, polaire , S, corde, masse, inertie, father)
        self.angleGouverne = 0
        self.pourcentageInfluenceGouverne = pourcentageInfluenceGouverne
        self.angleMaxGouverne = angleMaxGouverne
    
    def setBraquageGouverne(self, pourcentageBraquageGouverne):
        self.angleGouverne = pourcentageBraquageGouverne*self.angleMaxGouverne

    def getAlpha(self):
        alphaFixe = super().getAlpha() #Appelle SurfacePortante.getAlpha()
        return  alphaFixe + 0*self.angleGouverne*self.pourcentageInfluenceGouverne #DEBUUUUUUUUUUUUUUG
        
    def getTorseurEffortsAttachement(self):
        v = self.getVitesse().norm()
        alpha = self.getAlpha()
        torseurTot = self.getResultanteAero(alpha,v)
        print("emp v = ",v,"alpha = ", alpha," fzavion = ",torseurTot.getResultante().projectionRef(refAvion).getZ()," fxavion = ", torseurTot.getResultante().projectionRef(refAvion).getX(),"vZ = ", self.getVitesse().projectionRef(refAvion).getZ())
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
    def __init__(self):
        self.structure = Corps(T.Torseur(E.Vecteur(0,0,refAvion),E.Vecteur(0,0,refAvion),0),PM.masseTotal,PM.inertieTotal)   

        self.propulseur = Propulseur(E.Vecteur(PM.engine_x,PM.engine_z, refAvion),0,0,self.structure,0,PM.engineMaxThrust)
        self.structure.addAttachement(self.propulseur)

        #self.aileD = Aile(E.Vecteur(PM.ailesD_x_Foyer,PM.ailesD_z_Foyer,refAvion), 0, 0, self.structure, PM.aileD_S, PM.aileD_CzA, PM.aileD_Alpha_0, PM.aileD_Cx0, PM.aileD_k, 0, PM.flapsDPourcentage)
        #self.aileD = Aile(E.Vecteur(PM.ailesD_x_BA,PM.ailesD_z_BA,refAvion),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileD_S, PM.flapsDPourcentage, PM.flapsDMaxAngle, father = self.structure)
        #self.structure.addAttachement(self.aileD)

        #self.aileG = Aile(E.Vecteur(PM.ailesG_x_Foyer,PM.ailesG_z_Foyer,refAvion), 0, 0, self.structure, PM.aileG_S, PM.aileG_CzA, PM.aileG_Alpha_0, PM.aileG_Cx0, PM.aileG_k, 0, PM.flapsGPourcentage)
        #self.aileG = Aile(E.Vecteur(PM.ailesG_x_BA,PM.ailesG_z_BA,refAvion),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileG_S, PM.flapsGPourcentage, PM.flapsGMaxAngle, father = self.structure)
        #self.structure.addAttachement(self.aileG)

        #self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_Foyer,PM.empennageD_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageD_S,PM.empennageD_CzA, PM.empennageD_Alpha_0, PM.empennageD_Cx0, PM.empennageD_k,0 ,PM.elevDMaxAnglePourcentage)
        self.empennageD = Empennage(E.Vecteur(PM.empennageD_x_BA,PM.empennageD_z_BA,refAvion),PolaireLineaire(PM.empennageD_CzA, PM.empennageD_Alpha_0,PM.empennageD_Cx0, PM.empennageD_k,0),PM.empennageD_S,PM.empennageD_corde,PM.elevDPourcentage,PM.elevDMaxAngle,father= self.structure)
        self.structure.addAttachement(self.empennageD)

        #self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_Foyer,PM.empennageG_z_Foyer,refAvion), 0, 0, self.structure, PM.empennageG_S,PM.empennageG_CzA, PM.empennageG_Alpha_0, PM.empennageG_Cx0, PM.empennageG_k,0 ,PM.elevGMaxAnglePourcentage)
        self.empennageG = Empennage(E.Vecteur(PM.empennageG_x_BA,PM.empennageG_z_BA,refAvion),PolaireLineaire(PM.empennageG_CzA, PM.empennageG_Alpha_0,PM.empennageG_Cx0, PM.empennageG_k,0),PM.empennageG_S,PM.empennageG_corde,PM.elevGPourcentage,PM.elevGMaxAngle,father= self.structure)
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
        return self.structure.getTorseurCinematique().setResultante(E.Vecteur(vitessex,vitessez,refTerrestre))#TODO return ?????
    
    def diffuseDictRawInput(self,rawInputDict):
        #self.propulseur.setThrottlePercent(rawInputDict["throttle"])
        #self.aileD.setBraquageFlaps(rawInputDict["flapsD"])
        #self.aileG.setBraquageFlaps(rawInputDict["flapsG"])
        self.empennageD.setBraquageGouverne(rawInputDict["elevD"])
        self.empennageG.setBraquageGouverne(rawInputDict["elevG"])
        

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
    


       
    