from Scripts.Script import ScriptRaw
from DataTypes import RawInput,PilotInput,AutoPilotInput,FlightData
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

            out.setElevG(cos(0.1*(t-tStart) + dephasageElevatorGauche))
            out.setElevD(cos(0.1*(t-tStart)))

            if (out.getElevD()>0):
                flapsSorti = True
            else:
                flapsSorti = False

            if flapsSorti:
                out.setFlapsD(1)
                out.setFlapsG(1)
            else:
                out.setFlapsD(0)
                out.setFlapsG(0)

            out.setThrottle(0.5+0.5*cos((t-tStart)))

            self.publishData(out)
            time.sleep(1/frequence)



            