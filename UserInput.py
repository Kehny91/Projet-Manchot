class AutoPilotInput:
    def __init__(self, v, vz):
        self.v = v
        self.vz = vz

class PilotInput:
    def __init__(self,pitch,flaps,throttle):
        self.pitch = pitch
        self.flaps = flaps
        self.throttle = throttle

class RawInput:
    def __init__(self, elev1, elev2, flaps1, flaps2, throttle):
        self.elev1 = elev1
        self.elev2 = elev2
        self.flaps1 = flaps1
        self.flaps2 = flaps2
        self.throttle = throttle