'''
Created on 21 Jan 2014

@author: annes
'''
from libsbml import SBMLReader, SBMLWriter


def sbmlFileHasErrors(sbml_file):
    reader = SBMLReader()
    document = reader.readSBMLFromString(sbml_file)
    number_of_errors = document.getNumErrors()
    has_errors = number_of_errors > 0
    listOfErrors = []
    if number_of_errors:
        for error in range(number_of_errors):
            listOfErrors.append(document.getErrorLog().getError(error).getMessage())

    return [has_errors, listOfErrors]
