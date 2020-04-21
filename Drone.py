import Solide as S
import Espace as E
import SystemeMeca as Sy1O
from Parametres import ParametresModele as PM
from Parametres import ParametresSimulation as PS
from Polaire import PolaireLineaire,PolaireTabulee
from DataManagement import normalize


class Drone:
    """Permet de definir un drone
    \n attribute World : world, environement du drone
    \n attribute S.Solide :  corps, corps principal du drone
    \n attribute S.Propulseur : propulseur, attachement propulseur du drone
    \n attribute S.aile :  aileD, attachement aileD du drone
    \n attribute S.aile :  aileG, attachement aileG du drone
    \n attribute S.Empennage : EmpennageD, attachement empennageD du drone
    \n attribute S.Empennage : EmpennageG, attachement empennageG du drone
    \n des corps rigides
    """
    def __init__(self, world):
        self.world = world
        self.structure = S.Corps(S.refSol, E.Vecteur(0,0,S.refSol), 0, E.Vecteur(0,0,S.refSol), 0, world, PM.masseTotal, PM.inertieTotal)
        self.propulseur = S.Propulseur(E.Vecteur(PM.engine_x,PM.engine_z, self.structure), self.structure, 0, PM.engineMaxThrust, PM.engineMaxPow, Sy1O.Systeme1Ordre(0,0,PM.engineMaxThrust, PM.engine_tau))
        self.aileD = S.Aile(E.Vecteur(PM.ailesD_x_BA,PM.ailesD_z_BA,self.structure),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileD_S, PM.ailesD_corde, PM.flapsDPourcentageCordeArticulee,PM.flapsDPourcentageEnvergureArticulee, PM.flapsDMaxAngle, world, father = self.structure)
        self.aileG = S.Aile(E.Vecteur(PM.ailesG_x_BA,PM.ailesG_z_BA,self.structure),PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA"), PM.aileG_S, PM.ailesG_corde, PM.flapsGPourcentageCordeArticulee,PM.flapsGPourcentageEnvergureArticulee, PM.flapsGMaxAngle, world, father = self.structure)
        self.empennageD = S.Empennage(E.Vecteur(PM.empennageD_x_BA,PM.empennageD_z_BA, self.structure),PolaireTabulee("./XFLR5/CLtail","./XFLR5/CDtail","./XFLR5/CMtailBA"),PM.empennageD_S,PM.empennageD_corde,PM.elevDPourcentageCordeArticulee,PM.elevDPourcentageEnvergureArticulee,PM.elevDMaxAngle, PM.angleDemiDiedreEmpennageD, world,father= self.structure)
        self.empennageG = S.Empennage(E.Vecteur(PM.empennageG_x_BA,PM.empennageG_z_BA, self.structure),PolaireTabulee("./XFLR5/CLtail","./XFLR5/CDtail","./XFLR5/CMtailBA"),PM.empennageG_S,PM.empennageG_corde,PM.elevGPourcentageCordeArticulee,PM.elevGPourcentageEnvergureArticulee,PM.elevGMaxAngle, PM.angleDemiDiedreEmpennageG, world,father= self.structure)
       
        #Ajout des attachements sur le corps
        self.structure.addAttachement(self.propulseur)
        self.structure.addAttachement(self.aileD)
        self.structure.addAttachement(self.aileG)
        self.structure.addAttachement(self.empennageD)
        self.structure.addAttachement(self.empennageG)
        
        #definition et ajout des corps rigides sur le corps
        self.p1 = S.CorpsRigide(E.Vecteur(PM.p1_x,PM.p1_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p1",)
        self.structure.addCorpsRigide(self.p1)
        self.p2 = S.CorpsRigide(E.Vecteur(PM.p2_x,PM.p2_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p2")
        self.structure.addCorpsRigide(self.p2)
        self.p3 = S.CorpsRigide(E.Vecteur(PM.p3_x,PM.p3_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p3")
        self.structure.addCorpsRigide(self.p3)
        self.p4 = S.CorpsRigide(E.Vecteur(PM.p4_x,PM.p4_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p4")
        self.structure.addCorpsRigide(self.p4)
        self.p5 = S.CorpsRigide(E.Vecteur(PM.p5_x,PM.p5_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p5")
        self.structure.addCorpsRigide(self.p5)
        self.p6 = S.CorpsRigide(E.Vecteur(PM.p6_x,PM.p6_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p6")
        self.structure.addCorpsRigide(self.p6)
        self.p7 = S.CorpsRigide(E.Vecteur(PM.p7_x,PM.p7_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p7")
        self.structure.addCorpsRigide(self.p7)
        self.p8 = S.CorpsRigide(E.Vecteur(PM.p8_x,PM.p8_z,self.structure),self.structure,PS.maxAcceptablePenetrationSpeed, world, "p8")
        self.structure.addCorpsRigide(self.p8)

    #Methodes
    def diffuseDictRawInput(self,rawInputDict):
        """diffuse le dictionaire d Input, actualise les commandes"""
        self.propulseur.setThrottlePercent(rawInputDict["throttle"])
        self.aileD.setBraquageFlaps(rawInputDict["flapsD"])
        self.aileG.setBraquageFlaps(rawInputDict["flapsG"])
        self.empennageD.setBraquageGouverne(rawInputDict["elevD"])
        self.empennageG.setBraquageGouverne(rawInputDict["elevG"])

    def getPositionCG(self):
        return self.structure.getPositionCG()

    def getAssiette(self):
        return normalize(self.structure.getAngleAxeY())

    def getVitesseCG(self): 
        return self.structure.torseurCinematique.getVitesse()

    def getVitesseRot(self):
        return self.structure.torseurCinematique.getW()  

    def setPositionCG(self, newPosition):
        self.structure.setPositionCG(newPosition)
    
    def setAssiette(self, newAssiete):
        self.structure.setAngleAxeY(newAssiete)
    
    def setVitesseCG(self, newVitesse):
        self.structure.torseurCinematique.setVitesse(newVitesse)

    def setWCG(self, w):
        self.structure.torseurCinematique.setW(w)

    def getPositionBati(self):
        return self.propulseur.getPosition().changeRef(S.refSol)

    def getVitesseBati(self): 
        return self.propulseur.getVitesse().projectionRef(S.refSol)

    def setPositionBati(self, newPosition):
        self.setPositionCG(newPosition - self.propulseur.position.projectionRef(newPosition.getRef()))
    
    def setVitesseBati(self, newVitesse):
        tc = self.structure.torseurCinematique.changePoint(self.propulseur.position)
        tc.setVitesse(newVitesse)
        tc = tc.changePoint(self.getPositionCG())
        self.setVitesseCG(tc.getVitesse())

    def generateRapportCollision(self):
        """Produit un rapport de collision"""
        return self.structure.generateRapportCollision()

        