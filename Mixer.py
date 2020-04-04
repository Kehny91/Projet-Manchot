import UserInput as ui
import DataManagement as dm


class Mixer:
    @staticmethod
    def mix(pilotInput):
        out = ui.RawInput()
        # Les gouvernes sont utilisés en priorité pour l'elevator, ce qu'il reste est utilisé pour le yaw
        pitch = pilotInput.getPitch()
        
        #[3D]
        #placeRestante = 1 - abs(pitch)
        #yaw = dm.constrain(pilotInput.getYaw(),-placeRestante, placeRestante)
        yaw = 0
        
        out.setElevD(pitch + yaw)
        out.setElevG(pitch - yaw)

        out.setFlapsD(pilotInput.getFlaps())
        out.setFlapsG(pilotInput.getFlaps())

        out.setThrottle(pilotInput.getThrottle())

        return out