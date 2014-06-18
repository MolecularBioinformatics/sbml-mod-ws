from ZSI import Fault

from sbmlmod.SBMLmod_types import ns0

class SBMLmodFault(Fault):
    def __init__(self, message, faultEnum):
        self.message = message
        self.faultEnum = faultEnum
        response = ns0.SBMLmodFault_Dec().pyclass()
        response.set_element_FaultEnum(faultEnum)
        response.set_element_FaultMessage(message)
        Fault.__init__(self, Fault.Server, message, None, response)
      

      
