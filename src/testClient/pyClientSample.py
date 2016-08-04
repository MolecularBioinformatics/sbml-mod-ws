import base64
import logging
import zlib
import os
import warnings

import suds
from suds.client import Client

####
#
# exsample Client, which works purely localy
# PRE: server needs to run: ./bin/serverd start 
# 
# exemplarily an SBML is loaded, tested for validity and modified based on given data
# the resulting two sbml files are again tested for validity and written into new files
#
####

# wsdlURL DEPRECATED: works currently but needs to be updated as soon as service moved to Tromso
#wsdlURL			= 'http://cbu.bioinfo.no/wsdl/SBMLedit.wsdl'
# use local version, which gets shipped with the project
wsdlURL			= 'file://' + os.path.dirname(os.path.dirname( os.path.realpath(__file__) ))  + '/sbmlmod/SBMLmod.wsdl'
path			= './'
newSBMLbaseFilename	= 'newSBML'

# set compression or encoding to base64
# note that compress = True & encode = False is not supported and will be handled as compress = False, encode = False
compress = True
encode	 = True


def main():
	global path
	
	try:
		client   = set_client(False)
		
		logging.basicConfig(level=logging.INFO)
		logging.getLogger('suds.client').setLevel(logging.CRITICAL)	
	
		# get absolute path of running code
		path = os.path.dirname( os.path.realpath(__file__) ) + '/'
	
		# print minimal information about client
		print 'Client version: ', client.service.GetVersion()
		
		# get files and compress and encode them
		files   = get_files() # order: sbml, mapping, data
		ceFiles = compressAndEncode(files)
		
		# check model validity of base model
		print 'base SBML model validity status: '
		validateModel(client, ceFiles[0])
		
		# manipulate models by integrating dataset-specific values
		print 'Modifying model...'
		newModels = manipulateModels(client, ceFiles)
		
		# check model validity of new model
		print 'new SBML models validity status:'
		validateModel(client, newModels)
		
		# write resulting model to new file in current folder
		print 'Writing new model file(s) in folder' + os.getcwd()
		writeNewModelFile(client, newModels)
	
	except suds.WebFault as e:
		# show some log messages in case suds throws error  
		print('Last sent\n')
		print client.last_sent()
		print('\nLast received\n')
		print client.last_received()
		print('Error message:\n')
		print(e.fault)


# ================ #
# helper functions #
# ================ #

def writeNewModelFile(client, newModels):
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
		elif ( not compress and not encode ):
			newSBML = newModel
		else:
			io_warn()
			newSBML = newModel
		
		output.write(newSBML)
		output.close()
		print 'Completed.'
		

	
##
# example manipulation
# integrate E_T values from given dataset
#
def manipulateModels(client, files):
	sbml_files = []
	sbml_files.append(files[0])
	sbml_files.append(files[0])

	# build two new sbml files with replacing 'E_T' parameter values 
	
	if ( compress and encode ):
		newsbml = client.service.ReplaceGlobalParametersGzippedBase64Encoded(sbml_files,
															DataFile=files[2], DataColumnNumber=3,
															ParameterId="E_T",
															MappingFile=files[1], BatchMode=True)	
	elif ( not compress and encode ):
		newsbml = client.service.ReplaceGlobalParametersBase64Encoded(sbml_files,
															DataFile=files[2], DataColumnNumber=3,
															ParameterId="E_T",
															MappingFile=files[1], BatchMode=True)	
	elif ( ( not compress ) and ( not encode ) ):
		newsbml = client.service.ReplaceGlobalParametersText(sbml_files,
															DataFile=files[2], DataColumnNumber=3,
															ParameterId="E_T",
															MappingFile=files[1], BatchMode=True)	
	elif ( compress and not encode ):
		io_warn()
		newsbml = client.service.ReplaceGlobalParametersText(sbml_files,
															DataFile=files[2], DataColumnNumber=3,
															ParameterId="E_T",
															MappingFile=files[1], BatchMode=True)			
			
	return newsbml.SbmlModelFiles


##
# returns true if model is valid, false otherwise
#
def validateModel(client, models):
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
			## WARNING: calling client.service.ValidateSBMLModelGzippedBase64Encoded
			# throws server error on some system setups
			# if you want to check model validity first decode and decompress and check 
			# with client.service.ValidateSBMLModelText instead
			# This inconvenience will be resolved in a future release
			
			## not working, due to error thrown by from ZSI:
			# response = client.service.ValidateSBMLModelGzippedBase64Encoded(SbmlModelFile = model)
			
			# -> workaround by decoding and decompressing first and calling ValidateSBMLModelText instead:
			response = client.service.ValidateSBMLModelText( 
														SbmlModelFile = 
														zlib.decompress( base64.b64decode(model) ) )
			print 'Model is base64 encoded and compressed.'
		elif ( not compress and encode ):
			response = client.service.ValidateSBMLModelBase64Encoded(SbmlModelFile = model)
			print 'Model is base64 encoded.'
		elif ( ( not compress ) and ( not encode ) ):
			response = client.service.ValidateSBMLModelText(SbmlModelFile = model)
			print 'Model is not encoded or compressed.'
		elif ( compress and not encode ):
			io_warn()
			response = client.service.ValidateSBMLModelText(SbmlModelFile = model)
			print 'Model is not encoded or compressed.'	
		
		if response.ModelIsValid:
			print 'SBML model ', i, ' is valid.'
		else:
			print 'SBML model ', i, ' is not valid.'
		i += 1


##
# handles compression and encoding of example files
#
def compressAndEncode(files):
	ceFiles = []
	for i in range( 0, len(files) ):
		# in case model contains non ASCII literals, exchange with proper unicode
		tmp_file = ''.join([repr(c)[1:-1] if ord(c) > 128 else c for c in files[i]])	
		if ( compress and encode ):
			ceFiles.append( base64.b64encode(zlib.compress( tmp_file ) ) )				
		elif ( not compress and encode ):
			ceFiles.append( base64.b64encode( tmp_file ) )
		elif ( ( not compress ) and ( not encode ) ):	
			ceFiles.append( tmp_file )
		elif ( compress and not encode ):
			io_warn()
			ceFiles.append( tmp_file )
	
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
	
##
# simple warning message, in case user chooses wrong boolean setup (compress = False, encode = True is NOT allowed)
#
def io_warn():
    warnings.warn('User defined compression, but not encoding. Please check compression and encoding setup. Using no compression instead.', Warning)
	
if __name__ == '__main__':
    main()
