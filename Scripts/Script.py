import Modes as M

class _Script:
    mode = None
    def __init__(self, mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput):
        self._mddFlightData = mddFlightData
        self.flightData = mddFlightData.read()
        self.continuer = True
        self._mddOut = None
        

    def updateInputData(self):
        self.flightData = self._mddFlightData.read()

    def stop(self):
        self.continuer = False

    def reset(self):
        self.continuer = True

    def publishData(self, data):
        """ C'est cette méthode qui vous permettera d'émettre votre RawInput/PilotInput/AutoPilotInput"""

        assert self._mddOut!=None , "Il faut utiliser un ScriptRaw, ScriptPilot ou ScriptAutoPilot. Pas un '_Script'"
        self._mddOut.write(data)

    def runScript(self):
        """ C'est cette méthode qui est appellée lors du lancement du script.
            Pensez a appeller régulièrement updateInputData afin d'avoir des infos a jour
        """
        assert False, "Ce script est vide"

class ScriptRaw(_Script):
    mode = M.MODE_SCRIPT_RAW
    """ C'est un script qui écrit directement sur les raw input """
    def __init__(self, mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput):
        super(ScriptRaw,self).__init__(mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput)
        self._mddOut = mddRawInput

class ScriptPilot(_Script):
    mode = M.MODE_SCRIPT_PILOT
    """ C'est un script qui donne des commandes pilote """
    def __init__(self, mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput):
        super(ScriptPilot,self).__init__(mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput)
        self._mddOut = mddPilotInput

class ScriptAutoPilot(_Script):
    mode = M.MODE_SCRIPT_AUTOPILOT
    """ C'est un script qui donne des commandes a l'auto pilote """
    def __init__(self, mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput):
        super(ScriptAutoPilot,self).__init__(mddFlightData, mddRawInput, mddPilotInput, mddAutoPilotInput)
        self._mddOut = mddAutoPilotInput
