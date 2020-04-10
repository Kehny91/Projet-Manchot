import UserInput as ui
import DataManagement as dm


class Mixer:
    @staticmethod
    def mix(pilotInputMDD, rawInputMDD):
        # Les gouvernes sont utilisés en priorité pour l'elevator, ce qu'il reste est utilisé pour le yaw
        pitch = pilotInputMDD.getPitch()
        
        #[3D]
        #placeRestante = 1 - abs(pitch)
        #yaw = dm.constrain(pilotInput.getYaw(),-placeRestante, placeRestante)
        yaw = 0

        rawInputMDD.setElevD(pitch + yaw)
        rawInputMDD.setElevG(pitch - yaw)

        rawInputMDD.setFlapsD(pilotInputMDD.getFlaps())
        rawInputMDD.setFlapsG(pilotInputMDD.getFlaps())

        rawInputMDD.setThrottle(pilotInputMDD.getThrottle())


