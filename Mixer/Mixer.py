import Data.DataManagement as dm
from Data.DataTypes import PilotInput,RawInput

class Mixer:
    @staticmethod
    def mix(pilotInputMDD, rawInputMDD):
        # Les gouvernes sont utilisés en priorité pour l'elevator, ce qu'il reste est utilisé pour le yaw
        pilotIn = pilotInputMDD.read()
        pitch = pilotIn.getPitch()
        flaps = pilotIn.getFlaps()
        thr = pilotIn.getThrottle()

        out = RawInput()
        
        #[3D]
        #placeRestante = 1 - abs(pitch)
        #yaw = dm.constrain(pilotInput.getYaw(),-placeRestante, placeRestante)
        yaw = 0

        out.setElevD(pitch + yaw)
        out.setElevG(pitch - yaw)

        out.setFlapsD(flaps)
        out.setFlapsG(flaps)

        out.setThrottle(thr)

        rawInputMDD.write(out)


