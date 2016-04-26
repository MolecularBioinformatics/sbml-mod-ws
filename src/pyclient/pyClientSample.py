import base64
import logging
import zlib

from suds.client import Client

url 			= 'http://cbu.bioinfo.no/wsdl/SBMLedit.wsdl'
resource_folder = 'src/testsbmlmod/resources/'
newSBMLfilename = 'newSBML.xml'

def main():
	compress		= False
	encode			= True
	
	client = set_client(False)

	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.INFO)	
	print 'Client version: ', client.service.GetVersion()

	files   = get_files()
	ceFiles = compressAndEncode(files, compress, encode)
	
	print 'SBML model validity status: ', validateModel(client, ceFiles[0], compress, encode)
	
	newsbml = client.service.AddBoundsToKineticLaw(ceFiles[0], DefaultValue=1, DataColumnNumber=4, MergeMode='MIN', MappingFile=ceFiles[1], DataFile=ceFiles[3])

	print 'SBML model validity status: ', validateModel(client, newsbml, compress, encode)

# helper functions
# ================

def validateModel(client, model, compress, encode):
	if ( compress and encode ):
		response = client.service.ValidateSBMLModelGzippedBase64Encoded(SbmlModelFile = model)
	elif ( not compress and encode ):
		response = client.service.ValidateSBMLModelBase64Encoded(SbmlModelFile = model)
	
	return response


def compressAndEncode(files, compress, encode):
	if ( compress and encode ):
		ceSbmlFile     = base64.b64encode(zlib.compress(files[0]))
		ceMappingFile  = base64.b64encode(zlib.compress(files[1]))
		ceMappingFile2 = base64.b64encode(zlib.compress(files[2]))
		ceDataFile     = base64.b64encode(zlib.compress(files[3]))
	elif ( not compress and encode ):
		ceSbmlFile     = base64.b64encode(files[0])
		ceMappingFile  = base64.b64encode(files[1])
		ceMappingFile2 = base64.b64encode(files[2])
		ceDataFile     = base64.b64encode(files[3])
	
	return ceSbmlFile, ceMappingFile, ceMappingFile2, ceDataFile


def get_files():
	sbmlFile     = "".join(open(resource_folder + 'TRP_mammal_turnover_Oxy_GlobalParameters.xml', 'r'))
	mappingFile  = "".join(open(resource_folder + 'mapping_applied_rat.txt', 'r'))
	mappingFile2 = "".join(open(resource_folder + 'mappingRat_GlobalParameters.txt', 'r'))
	dataFile     = "".join(open(resource_folder + 'RotteBiweightAlleVev.txt', 'r'))
	
	return sbmlFile, mappingFile, mappingFile2, dataFile

	
def set_client(show):
	client = Client(url, cache=None)
	if show:
		print client
	return client
	
	
	
if __name__ == '__main__':
    main()
