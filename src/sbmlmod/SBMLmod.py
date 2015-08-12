from ZSI import ServiceContainer
import base64
import zlib

from libsbml import SBMLReader

from SBMLmod_server import SBMLmod
from sbmlmod.DataMapper import DataMapper
from sbmlmod.FilesIO import FilesIO    
from sbmlmod.ManipulateKineticParameters import ManipulateKineticParameters
from sbmlmod.ModelEditor import ModelEditor
from sbmlmod.SBMLmod_fault import SBMLmodFault
from sbmlmod.facades import ValidateSBMLmodel_facade
from sbmlmod.facades import version_facade


# from pyserver.config import WSDL
class SBMLmodWS(SBMLmod):
    '''
    classdocs
    '''


    # _wsdl = "".join(open(WSDL).readlines())

    # throughout the class different versions of model encoding/compression 
    # (plain text, base64, base64+zipped) are considered
    #   functions w/o suffix are kept for historical reasons and are equivalent to
    #   *GzippedBase64Encoded versions
    # --
    # all SOAP_ functions are according to wsdl definition 

    def soap_GetVersion(self, ps):
        request, response = SBMLmod.soap_GetVersion(self, ps)
        
        response.set_element_Version(version_facade.getVersion())
        return request, response
    
    # Validate that the SBML model is compatible with given sbml version
    # --
    def soap_ValidateSBMLModel(self, ps):
        return self.soap_ValidateSBMLModelGzippedBase64Encoded(self, ps)

    def soap_ValidateSBMLModelText(self, ps):
        request, response = SBMLmod.soap_ValidateSBMLModelText(self, ps)
        
        sbml_file = request.get_element_SbmlModelFile()
        self.checkSBMLFileForErrors(response, sbml_file)

        return request, response

    def soap_ValidateSBMLModelBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ValidateSBMLModelBase64Encoded(self, ps)
        
        sbml_file = base64.b64decode(request.get_element_SbmlModelFile())
        self.checkSBMLFileForErrors(response, sbml_file)
        return request, response

    def soap_ValidateSBMLModelGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ValidateSBMLModelGzippedBase64Encoded(self, ps)
        
        sbml_file = request.get_element_SbmlModelFile()

        try:
            sbml_file = zlib.decompress(base64.b64decode(request.get_element_SbmlModelFile()))
        except:
            message = "File could not be decompressed, ensure file is not empty and that file is zipped and then encoded as a string."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        self.checkSBMLFileForErrors(response, sbml_file)

        return request, response    

    def checkSBMLFileForErrors(self, response, sbml_file):

        [has_errors, listOfErrors] = ValidateSBMLmodel_facade.sbmlFileHasErrors(sbml_file)
        response.set_element_ModelIsValid(not has_errors)
        if has_errors:
            response.set_element_ErrorMessages(listOfErrors)            
    
    # --
    
    # replace kinetic law parameters
    # --
    # this function is kept for historical reasons, if end-users are accessing still via 1. gen. realisation of this function
    # which in fact is resembled by the zipped and base64 encoded version
    def soap_ReplaceKineticLawParameter(self, ps):
        return self.soap_ReplaceKineticLawParameterGzippedBase64Encoded(self, ps)

    def soap_ReplaceKineticLawParameterText(self, ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameterText(self, ps)
        files = self.getFilesAsText(request)
        results, warnings = ManipulateKineticParameters.replaceKineticLawParameter(request, files)
        
        response.set_element_SbmlModelFiles(FilesIO.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response
    
    def soap_ReplaceKineticLawParameterBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameterBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64(request)
        results, warnings = ManipulateKineticParameters.replaceKineticLawParameter(request, files)
        
        response.set_element_SbmlModelFiles(FilesIO.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceKineticLawParameterGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameterGzippedBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64Gunzip(request)
        results, warnings = ManipulateKineticParameters.replaceKineticLawParameter(request, files)
        
        response.set_element_SbmlModelFiles(FilesIO.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response
    
    # --

    # scale kinetic para section
    # --
    def soap_ScaleKineticLawParameter(self, ps):
        return self.soap_ScaleKineticLawParameterGzippedBase64Encoded(self, ps)
    
    def soap_ScaleKineticLawParameterText(self, ps):

        request, response = SBMLmod.soap_ScaleKineticLawParameterText(self, ps)
        
        files = FilesIO.getFilesAsText(request)
        results, warnings = ManipulateKineticParameters.scaleKineticLawParameter(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ScaleKineticLawParameterBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ScaleKineticLawParameterBase64Encoded(self, ps)
        files = FilesIO.getFilesDecodeBase64(request)

        results, warnings = ManipulateKineticParameters.scaleKineticLawParameter(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ScaleKineticLawParameterGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ScaleKineticLawParameterGzippedBase64Encoded(self, ps)
        files = FilesIO.getFilesDecodeBase64Gunzip(request)

        results, warnings = ManipulateKineticParameters.scaleKineticLawParameter(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    # --

    # add kinetic laws
    # --
    def soap_AddKineticLawParameter(self, ps):
        request, response = SBMLmod.soap_AddKineticLawParameter(self, ps)
        return ManipulateKineticParameters.addKineticLawParameter(request, response)

    # --

    # add bounds to kinetic laws
    # --
    def soap_AddBoundsToKineticLaw(self, ps):
        return self.soap_AddBoundsToKineticLawGzippedBase64Encoded(self, ps)
        
    def soap_AddBoundsToKineticLawText(self, ps):
        request, response = SBMLmod.soap_AddBoundsToKineticLawText(self, ps)
        files = self.getFilesAsText(request)

        results, warnings = ManipulateKineticParameters.addBoundsToKineticLaw(self, request, files)

        response.set_element_SbmlModelFiles(FilesIO.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_AddBoundsToKineticLawBase64Encoded(self, ps):
        request, response = SBMLmod.soap_AddBoundsToKineticLawBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64(request)

        results, warnings = ManipulateKineticParameters.addBoundsToKineticLaw(self, request, files)

        response.set_element_SbmlModelFiles(FilesIO.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_AddBoundsToKineticLawGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_AddBoundsToKineticLawGzippedBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64Gunzip(request)

        results, warnings = ManipulateKineticParameters.addBoundsToKineticLaw(self, request, files)
        
        response.set_element_SbmlModelFiles(FilesIO.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    # --

    # replace initial concentrations of model species

    def soap_ReplaceInitialConcentrationsOfSpecies(self, ps):
        return self.soap_ReplaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(self, ps)

    def soap_ReplaceInitialConcentrationsOfSpeciesText(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpeciesText(self, ps)
        files = self.getFilesText(request)

        results, warnings = ManipulateKineticParameters.replaceInitialConcentrationsOfSpecies(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceInitialConcentrationsOfSpeciesBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpeciesBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64(request)

        results, warnings = ManipulateKineticParameters.replaceInitialConcentrationsOfSpecies(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64Gunzip(request)

        results, warnings = ManipulateKineticParameters.replaceInitialConcentrationsOfSpecies(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    # --

    # replace global parameters

    def soap_ReplaceGlobalParameters(self, ps):
        return self.soap_ReplaceGlobalParametersGzippedBase64Encoded(self, ps)


    def soap_ReplaceGlobalParametersText(self, ps):
        request, response = SBMLmod.soap_ReplaceGlobalParametersText(self, ps)
        files = self.getFilesAsText(request)

        results, warnings = ManipulateKineticParameters.replaceGlobalParameters(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceGlobalParametersBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceGlobalParametersBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64(request)
        results, warnings = ManipulateKineticParameters.replaceGlobalParameters(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceGlobalParametersGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceGlobalParametersGzippedBase64Encoded(self, ps)
        files = self.getFilesDecodeBase64Gunzip(request)

        results, warnings = ManipulateKineticParameters.replaceGlobalParameters(self, request, files)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    # --



    def soap_ScaleGlobalParametersText(self, ps):
        request, response = SBMLmod.soap_ScaleGlobalParametersText(self, ps)
        return self.scaleGlobalParametersText(request, response)

    def scaleGlobalParametersText(self, request, response):

        files = self.getFilesAsText(request)

        sbmlfiles = files[0]
        datafile = files[1]
        mappingfile = files[2]

        results, warnings = self.executeScaleGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ScaleGlobalParametersBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ScaleGlobalParametersBase64Encoded(self, ps)
        return self.scaleGlobalParametersBase64Encoded(request, response)


    def scaleGlobalParametersBase64Encoded(self, request, response):
        files = self.getFilesDecodeBase64(request)
        sbmlfiles = files[0]
        datafile = files[1]
        mappingfile = files[2]

        results, warnings = self.executeScaleGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ScaleGlobalParametersGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ScaleGlobalParametersGzippedBase64Encoded(self, ps)
        return self.scaleGlobalParametersGzippedBase64Encoded(request, response)


    def scaleGlobalParametersGzippedBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles = files[0]
        datafile = files[1]
        mappingfile = files[2]

        results, warnings = self.executeScaleGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def executeScaleGlobalParameters(self, request, sbmlfiles, datafile, mappingfile):

        mapper = DataMapper()
        warnings = []

        datacolumn = 2

        if request.get_element_DataColumnNumber():
            datacolumn = int(request.get_element_DataColumnNumber())

        batch = request.get_element_BatchMode()

        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile) - datacolumn + 1:
                message = "The there are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one file can be submitted when batch mode is set to False"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        if mappingfile != None:
            mapper.setup(mappingfile, datafile, datacolumn, batch=batch)
            if request.get_element_MergeMode():
                mergemode = request.get_element_MergeMode()
                result = mapper.mergeExpressionValuesMappingToSameReaction(mode=mergemode)
            else:

                result = mapper.mergeExpressionValuesMappingToSameReaction()

            self.expr = result[0]
            self.exprId = result[1]
            warnings = result[2]

        else:
            self.expr, self.exprId = mapper.setup_expr(datafile, datacolumn, batch=batch)


        # SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass

        newsbmlfiles = []
        header = self.getDataHeader(datafile, datacolumn)
        editor = ModelEditor()

        if batch:

            if len(sbmlfiles) > 1:


                for i in range(len(sbmlfiles)):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                    if sbmlDocument.getNumErrors():
                        message = "The SBML file is not valid."
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                    newModel, warnings = editor.scaleGlobalParameters(document=sbmlDocument, data=self.expr, column=i, datainfo=self.exprId, warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlfiles.append(sbmlDocument)

            else:
                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                for i in range(len(self.expr[0])):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                    newModel, warnings = editor.scaleGlobalParameters(document=sbmlDocument, data=self.expr, column=i, datainfo=self.exprId, warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlfiles.append(sbmlDocument)



        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            newModel, warnings = editor.scaleGlobalParameters(document=sbmlDocument, data=self.expr, column=0, datainfo=self.exprId, warnings=warnings)

            sbmlDocument.setModel(newModel)
            newsbmlfiles.append(sbmlDocument)


        return [newsbmlfiles, header], warnings


    def getMappingFile(self, request):
        try:
            mappingfile = zlib.decompress(base64.b64decode(request.get_element_MappingFile())).strip()
        except:
            message = "The mapping file could not be decompressed, ensure file is not emtpy, zipped and then encoded as a string."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        return mappingfile

    def getSBMLFile(self, request):
        sbmlfiles = []

        files = request.get_element_SbmlModelFiles()

        for f in files:
            try:
                sbmlfiles.append(zlib.decompress(base64.b64decode(f)).strip())
            except:
                message = "The SBML model could not be decompressed, ensure file is not empty, zipped and then encoded as a string."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        return sbmlfiles

    def getDataFile(self, request):
        try:
            datafile = zlib.decompress(base64.b64decode(request.get_element_DataFile())).strip()
        except:
            message = "The data file could not be decompressed, ensure file is not empty, zipped and then encoded as a string."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        return datafile

    def isTabDelimitedAndAllRowsContainEqualNumberOfColumns(self, datafile):
        lines = datafile.split('\n')

        firstcolno = 0
        first = True

        for i in range(1, len(lines)):
            line = lines[i]
            if not first:
                colno = line.count('\t')

                if colno == 0:
                    return False
                if colno != firstcolno:
                    return False
            else:
                firstcolno = line.count('\t')
                if firstcolno == 0:
                    return False
                first = False
        return True

    def getDataHeader(self, datafile, col=2):
        line = datafile.split('\n')[0]
        columns = line.split('\t')
        header = []

        for i in range(col - 1, len(columns)):
            header.append(columns[i])

        return header



    def getOption(self, request):
        option1 = 'INSERT_DEFAULT'
        option2 = 'INSERT_DATA_THEN_DEFAULT'
        option3 = 'INSERT_DATA_WITH_MAPPING_THEN_DEFAULT'
        option = None

        if request.get_element_DataFile():
            if request.get_element_MappingFile():
                option = option3
            else:
                option = option2

        elif request.get_element_DefaultValue():
            option = option1

        return option


    


def main():
    port = 8080
    address = ('', port)
    sc = ServiceContainer.ServiceContainer(address, [SBMLmodWS()])
    sc.serve_forever()

if __name__ == '__main__':
    main()
