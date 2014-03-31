'''
Created on Nov 12, 2010

@author: mblso
'''
from ZSI import Fault

from sbmledit.SBMLEdit_types import ns0

class SBMLEditFault(Fault):
    def __init__(self, message, faultEnum):
        self.message = message
        self.faultEnum = faultEnum
        response = ns0.SBMLEditFault_Dec().pyclass()
        response.set_element_FaultEnum(faultEnum)
        response.set_element_FaultMessage(message)
        Fault.__init__(self, Fault.Server, message, None, response)
      

      
