import UserInput as ui
import DataManagement as dm
import Mixer as mx


"""
if __name__ == "__main__":
    rawInput = ui.RawInput(0,0,0,0,0)
    rawInput.setElevD(-1)
    rawInput.setElevG(-0.8)
    rawInput.setFlapsD(0.1)
    rawInput.setFlapsG(0.3)
    rawInput.setThrottle(0.5)
    print(str(rawInput.__dict__))
    try:
        rawInput.setFlapsD(-0.1)
    except dm.OutOfBoundException:
        print("Unauthorized")

    pilotInput = ui.PilotInput(0,0,0)
    pilotInput.setFlaps(0.1)
    pilotInput.setPitch(0.2)
    pilotInput.setThrottle(0.3)
    print(str(pilotInput.__dict__))
    try:
        pilotInput.setThrottle(1.1)
    except:
        print("Unauthorized")

    autoPilotInput = ui.AutoPilotInput(0,0)
    autoPilotInput.setV(0.1)
    autoPilotInput.setVz(-0.1)
    print(str(autoPilotInput.__dict__))
"""

if __name__ == "__main__":
    pilotInput = ui.PilotInput(1,0.5,0.8)
    rawInput = mx.Mixer.mix(pilotInput)
    print(rawInput.__dict__)
