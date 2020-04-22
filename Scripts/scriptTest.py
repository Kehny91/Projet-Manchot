from Scripts.Script import ScriptRaw,ScriptAutoPilot
from Data.DataTypes import RawInput,PilotInput,AutoPilotInput,FlightData
from Physique.Espace import Vecteur
from math import pi,cos
import time

class ScriptExemple(ScriptRaw):

    def runScript(self):
        tStart = time.time() #On garde en tete l'heure du lancement du script
        dephasageElevatorGauche = pi/2
        flapsSorti = False
        frequence = 40 #Hz

        while self.continuer:

            t = time.time() # On regarde l'heure actuelle
            self.updateInputData() #On met a jour self.flightData (on ne l'utilise pas ici)

            out = RawInput() #On cree notre objet de sortie. (un rawInput ici)

            out.setElevG(cos(0.3*(t-tStart) + dephasageElevatorGauche)) #On donne le pourcentage de braquage de l'elevator gauche
            out.setElevD(cos(0.3*(t-tStart)))                           #On donne le pourcentage de braquage de l'elevator droit

            if (out.getElevD()>0): #Si on a un braquage positif de l'elevator droit
                flapsSorti = True  #La variable flapsSorti est vraie
            else:
                flapsSorti = False

            if flapsSorti:        #Si la variable flapsSorti est vraie
                out.setFlapsD(1)  #On braque le flap droit a 100%
                out.setFlapsG(1)  #On braque le flap droit a 100%
            else:                 #Sinon
                out.setFlapsD(0)  #On rentre le flap droit a 0%
                out.setFlapsG(0)  #On rentre le flap gauche a 0%

            out.setThrottle(0.5+0.5*cos((t-tStart))) #On donne le pourcentage de gaz

            self.publishData(out) #On envoie cela au modèle
            time.sleep(1/frequence) #On lière un peu le CPU


class ScriptLanding(ScriptAutoPilot):
    
    def runScript(self):
        tStart = time.time() #On garde en tete l'heure du lancement du script
        dephasageElevatorGauche = pi/2
        flapsSorti = False
        frequence = 40 #Hz

        while self.continuer:

            t = time.time() # On regarde l'heure actuelle
            self.updateInputData() #On met a jour self.flightData (on ne l'utilise pas ici)

            out = AutoPilotInput() #On cree notre objet de sortie. (un autopilot ici)

            if (self.flightData.getPosAvion().getZ()>1):
                print("descente")
                out.setVx(10)
                out.setVz(-2)
            else:
                print("arrondi")
                out.setVx(0)
                out.setVz(-0.1)

            self.publishData(out) #On envoie cela au modèle
            time.sleep(1/frequence) #On lière un peu le CPU



            