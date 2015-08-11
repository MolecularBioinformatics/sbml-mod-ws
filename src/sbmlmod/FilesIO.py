'''
Created on Jul 3, 2015

@author: schaeuble
'''

import base64
import zlib

from libsbml import SBMLReader, SBMLWriter

from sbmlmod.SBMLmod_fault import SBMLmodFault
from sbmlmod.SBMLmod_types import ns0 as SBMLfiletypeNs


class FilesIO(object):
    '''
    classdocs
    '''

    def getFilesAsText(self, request):
        sbmlfiles = request.get_element_SbmlModelFiles()

        for f in sbmlfiles:
            reader = SBMLReader()
            document = reader.readSBMLFromString(f)
            if document.getNumErrors():
                message = "Invalid SBML file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        datafile = None
        if request.get_element_DataFile():
            datafile = request.get_element_DataFile()
            
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        mappingfile = None
        if request.get_element_MappingFile():
            mappingfile = request.get_element_MappingFile()
            
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        return [sbmlfiles, datafile, mappingfile]

    def getFilesDecodeBase64(self, request):

        files = request.get_element_SbmlModelFiles()
        sbmlfiles = []

        for f in files:
            reader = SBMLReader()
            f = base64.b64decode(f).strip()
            document = reader.readSBMLFromString(f)
            if document.getNumErrors():
                message = "Invalid SBML file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            sbmlfiles.append(f)

        datafile = None
        if request.get_element_DataFile():
            datafile = request.get_element_DataFile()
            datafile = base64.b64decode(datafile).strip()

            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        mappingfile = None
        if request.get_element_MappingFile():
            mappingfile = request.get_element_MappingFile()
            mappingfile = base64.b64decode(mappingfile).strip()

            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        return [sbmlfiles, datafile, mappingfile]


    def getFilesDecodeBase64Gunzip(self, request):

        sbmlfiles = self.getSBMLFile(request)

        datafile = None
        if request.get_element_DataFile():
            datafile = self.getDataFile(request)

            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        mappingfile = None
        if request.get_element_MappingFile():
            mappingfile = self.getMappingFile(request)
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        return [sbmlfiles, datafile, mappingfile]
    
    def writeResultsToFileGzippedBase64Encoded(self, results):

        SBMLmod_file = SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod", "SbmlModelFilesType")).pyclass
        sbmlDocuments = results[0]
        header = results[1]

        writtenFiles = []

        for i in range(len(sbmlDocuments)):
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name(header[i])
            sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocuments[i]))))
            writtenFiles.append(sbmlEditfile)

        return writtenFiles

    def writeResultsToFileBase64Encoded(self, results):

        SBMLmod_file = SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod", "SbmlModelFilesType")).pyclass
        sbmlDocuments = results[0]
        header = results[1]

        writtenFiles = []

        for i in range(len(sbmlDocuments)):
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name(header[i])
            sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(writer.writeSBMLToString(sbmlDocuments[i])))
            writtenFiles.append(sbmlEditfile)

        return writtenFiles

    def writeResultsToFileText(self, results):
        SBMLmod_file = SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod", "SbmlModelFilesType")).pyclass
        sbmlDocuments = results[0]
        header = results[1]

        writtenFiles = []

        for i in range(len(sbmlDocuments)):
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name(header[i])
            sbmlEditfile.set_element_SbmlModelFile(writer.writeSBMLToString(sbmlDocuments[i]))
            writtenFiles.append(sbmlEditfile)


        return writtenFiles
            
