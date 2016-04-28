import base64
import logging
import zlib
import os

from suds.client import Client

wsdlURL 			= 'http://cbu.bioinfo.no/wsdl/SBMLedit.wsdl'
path 				= './'
newSBMLbaseFilename = 'newSBML'

def main():
	compress		= True
	encode			= True
	
	client = set_client(False)

	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.CRITICAL)	

	# print minimal information about client
	print 'Client version: ', client.service.GetVersion()
	
	# get files and compress and encode them
	files   = get_files() # order: sbml, mapping, data
	ceFiles = compressAndEncode(files, compress, encode)
	
	# check model validity of base model
	print 'base SBML model validity status: ' 
	#validateModel(client, ceFiles[0], compress, encode)
	
	# manipulate models by integrating dataset-specific values
	print 'Modifying network...'
	newModels = manipulateModels(client, ceFiles)
	
	# check model validity of new model
	print 'new SBML models validity status:'
	validateModel(client, newModels, compress, encode)
	
	# write resulting model to new file in current folder
	print 'Writing new model(s) to ' + os.getcwd()
	writeNewModelFile(client, newModels, compress, encode)
	
	print 'Done.'



# ================ #
# helper functions #
# ================ #

def writeNewModelFile(client, newModels, compress, encode):
	# check whether single model as string or response and list thus, list structure from webservice is given
	response = True
	if isinstance(newModels, basestring):
		foo=[]
		foo.append(newModels)
		newModels = foo
		response = False

	for newModel in newModels:
		if response:
			name     = newModel.Name
			newModel = newModel.SbmlModelFile			
			
		print 'Writing \'' + newSBMLbaseFilename + '_' + name + '.xml\''
		output = open(path + newSBMLbaseFilename + '_' + name + '.xml', 'w')
		if ( compress and encode ):
			newSBML = zlib.decompress( base64.b64decode(newModel) )
		elif ( not compress and encode ):
			newSBML = base64.b64decode(newModel)	
		
		output.write(newSBML)
		output.close()
		print 'Done.'
		

	
##
# example manipulation
# integrate E_T values from given dataset
#
def manipulateModels(client, files):
	sbml_files = []
	sbml_files.append(files[0])
	sbml_files.append(files[0])
	
	newsbml = client.service.ReplaceGlobalParametersGzippedBase64Encoded(sbml_files, 
																		DataFile=files[2], DataColumnNumber=3,
																		ParameterId="E_T",
																		MappingFile=files[1], BatchMode=True)
	response = client.service.AddBoundsToKineticLawGzippedBase64Encoded(newsbml.SbmlModelFiles[0].SbmlModelFile,
																	DataFile = files[2], DefaultValue=999, 
																	DataColumnNumber=10, MappingFile=files[1],
																	BatchMode=False)
	newsbml.SbmlModelFiles[0] = response.SbmlModelFiles[0]
		
	return newsbml.SbmlModelFiles


##
# returns true if model is valid, false otherwise
#
def validateModel(client, models, compress, encode):
	# check whether single model as string or response and list thus, list structure from webservice is given
	response = True
	if isinstance(models, basestring):
		foo=[]
		foo.append(models)
		models = foo
		response = False
		
	i = 1
	for model in models:
		if response:
			model = model.SbmlModelFile
					
		if ( compress and encode ):
			response = client.service.ValidateSBMLModelGzippedBase64Encoded(SbmlModelFile = model)
			print 'Model is base64 encoded and compressed.'
		elif ( not compress and encode ):
			response = client.service.ValidateSBMLModelBase64Encoded(SbmlModelFile = model)
			print 'Model is base64 encoded.'
		elif ( not ( compress and encode ) ):
			response = client.service.ValidateSBMLModelText(SbmlModelFile = model)
			print 'Model is not encoded or compressed.'
		
		if response.ModelIsValid:
			print 'SBML model ', i, ' is valid.'
		else:
			print 'SBML model ', i, ' is not valid.'
		i += 1


##
# handles compression and encoding of working files
#
def compressAndEncode(files, compress, encode):
	ceFiles = []
	for i in range( 0, len(files) ):
		if ( compress and encode ):
			ceFiles.append( base64.b64encode(zlib.compress( files[i] ) ) )
		elif ( not compress and encode ):
			ceFiles.append( base64.b64encode( files[i] ) )
	
	return ceFiles


##
# returns file array in the order sbml, mapping, data
#
def get_files():
	sbmlFile     = "".join(open(path + 'TRP_mammal.xml', 'r'))
	mappingFile  = "".join(open(path + 'mappingRat_GlobalParameters.txt', 'r'))
	dataFile     = "".join(open(path + 'rat_expr_multipleTissues.txt', 'r'))
	
	return sbmlFile, mappingFile, dataFile


##
# if show is true, full dump of client to commandline
#	
def set_client(show):
	client = Client(wsdlURL, cache=None)
	if show:
		print client
	return client
	
	
	
if __name__ == '__main__':
    main()
