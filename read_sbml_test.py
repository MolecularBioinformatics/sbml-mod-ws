from libsbml import *

def main():
	reader = SBMLReader()
	document = reader.readSBML("/Users/mblso/projects/esysbio/services-bio-incubator/sbmlmapping/src/test/resources/not_valid.sbml")
	print(document.getNumErrors())
	