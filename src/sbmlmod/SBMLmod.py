from SBMLmod_server import SBMLmod
#from pyserver.config import WSDL
from ZSI import ServiceContainer
import base64
import zlib
import tarfile
from libsbml import SBMLReader, SBMLWriter
from sbmlmod.SBMLmod_fault import SBMLmodFault
from sbmlmod.DataMapper import DataMapper
from sbmlmod.ModelEditor import ModelEditor
import StringIO
from sbmlmod.SBMLmod_types import ns0 as SBMLfiletypeNs

from sbmlmod.facades import version_facade
from sbmlmod.facades import ValidateSBMLmodel_facade

class SBMLmodWS(SBMLmod):
    '''
    classdocs
    '''


    #_wsdl = "".join(open(WSDL).readlines())


    def soap_GetVersion(self, ps):
        request, response = SBMLmod.soap_GetVersion(self, ps)
        
        response.set_element_Version(version_facade.getVersion())
        return request, response
    
    # handle different versions of model imports (plain text, zipped and/or base64 encoded)
    # --
    
    # this method is still included for historical reasons and to still support downstream usage,
    # if users build up on it
    # the content is equivalent to soap_ValidateSBMLModelGzippedBase64Encoded
    def soap_ValidateSBMLModel(self, ps):
        return self.soap_ValidateSBMLModelGzippedBase64Encoded(ps)

    def soap_ValidateSBMLModelText(self, ps):
        request, response = SBMLmod.soap_ValidateSBMLModelText(self, ps)
        
        sbml_file = request.get_element_SbmlModelFile()
        self.checkSBMLFileForErrors(response, sbml_file)

        return request, response

    def soap_ValidateSBMLModelBase64Encoded(self,ps):
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
            
            

    def soap_ReplaceKineticLawParameter(self, ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameter(self, ps)
        
        datafile = self.getDataFile(request)
        sbmlfiles = self.getSBMLFile(request)

        if request.get_element_MappingFile():
            mappingfile = self.getMappingFile(request)
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:                
            mappingfile = None

        if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
            message = "The data file is not tab delimited or rows contain unequal number of columns."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        results,warnings= self.executeReplaceKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def getFilesAsText(self,request):

        sbmlfiles = request.get_element_SbmlModelFiles()

        for file in sbmlfiles:
            reader = SBMLReader()
            document = reader.readSBMLFromString(file)
            if document.getNumErrors():
                message = "Invalid SBML file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        datafile=None

        if request.get_element_DataFile():
            datafile = request.get_element_DataFile()


            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        mappingfile=None

        if request.get_element_MappingFile():

            mappingfile = request.get_element_MappingFile()
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        return [sbmlfiles, datafile, mappingfile]

    def getFilesDecodeBase64(self,request):

        files = request.get_element_SbmlModelFiles()
        sbmlfiles=[]

        for file in files:
            reader = SBMLReader()
            file  = base64.b64decode(file).strip()
            document = reader.readSBMLFromString(file)
            if document.getNumErrors():
                message = "Invalid SBML file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            sbmlfiles.append(file)

        datafile=None

        if request.get_element_DataFile():
            datafile = request.get_element_DataFile()
            datafile = base64.b64decode(datafile).strip()

            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        mappingfile=None

        if request.get_element_MappingFile():
            mappingfile = request.get_element_MappingFile()
            mappingfile = base64.b64decode(mappingfile).strip()

            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        return [sbmlfiles, datafile, mappingfile]


    def getFilesDecodeBase64Gunzip(self,request):

        sbmlfiles = self.getSBMLFile(request)

        datafile=None

        if request.get_element_DataFile():
            datafile = self.getDataFile(request)

            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        mappingfile=None

        if request.get_element_MappingFile():
            mappingfile = self.getMappingFile(request)
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        return [sbmlfiles, datafile, mappingfile]

    def soap_ReplaceKineticLawParameterText(self,ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameterText(self, ps)
        return self.replaceKineticLawParameterText(request, response)

    def replaceKineticLawParameterText(self, request, response):
        files = self.getFilesAsText(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceKineticLawParameterBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameterBase64Encoded(self, ps)
        return self.replaceKineticLawParameterBase64Encoded(request, response)


    def replaceKineticLawParameterBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_ReplaceKineticLawParameterGzippedBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ReplaceKineticLawParameterGzippedBase64Encoded(self, ps)
        return self.replaceKineticLawParameterGzippedBase64Encoded(request, response)


    def replaceKineticLawParameterGzippedBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def executeReplaceKineticLawParameter(self, request, sbmlfiles, datafile, mappingfile):
        if not request.get_element_ParameterId():
            message = "Please state which parameter to scale."
            raise SBMLmodFault(message, "MISSING_ELEMENT")

        mapper = DataMapper()
        warnings=[]

        datacolumn=2
        if request.get_element_DataColumnNumber():
            datacolumn=int(request.get_element_DataColumnNumber())

        batch = False
        if request.get_element_BatchMode():
            batch = request.get_element_BatchMode()

        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                message = "The there are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one model file can be submitted when batch mode is set to False"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")



        if mappingfile != None:

            mapper.setup(mappingfile, datafile, datacolumn,batch=batch)

            if request.get_element_MergeMode():
                mergemode = request.get_element_MergeMode()
                result = mapper.mergeExpressionValuesMappingToSameReaction(mode=mergemode)
            else:

                result = mapper.mergeExpressionValuesMappingToSameReaction()


            self.expr = result[0]
            self.exprId = result[1]
            warnings = result[2]

        else:
            if request.get_element_DataColumnNumber():
                datacolumn=int(request.get_element_DataColumnNumber())
                self.expr,self.exprId = mapper.setup_expr(datafile, datacolumn,batch=batch)
            else:
                self.expr,self.exprId = mapper.setup_expr(datafile,batch=batch)



        newmodels=[]
        header = self.getDataHeader(datafile,datacolumn)
        editor = ModelEditor()


        if batch:

            if len(sbmlfiles)>1:


                for i in range(len(sbmlfiles)):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                    if sbmlDocument.getNumErrors():
                        message = "The SBML file is not valid."
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                    newModel, warnings = editor.replaceKineticLawParameter(document = sbmlDocument, data=self.expr, column=i,datainfo=self.exprId,parameter=request.get_element_ParameterId(), warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newmodels.append(sbmlDocument)


            else:
                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                for i in range(len(self.expr[0])):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                    newModel, warnings = editor.replaceKineticLawParameter(document = sbmlDocument, data=self.expr, column=i,datainfo=self.exprId,parameter=request.get_element_ParameterId(), warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newmodels.append(sbmlDocument)


        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            newModel, warnings = editor.replaceKineticLawParameter(document = sbmlDocument, data=self.expr, column=0,datainfo=self.exprId,parameter=request.get_element_ParameterId(), warnings=warnings)

            sbmlDocument.setModel(newModel)
            newmodels.append(sbmlDocument)


        return [newmodels,header],warnings

    def soap_ScaleKineticLawParameter(self, ps):
        request, response = SBMLmod.soap_ScaleKineticLawParameter(self, ps)
        return self.scaleKineticLawParameter(request, response)
    def scaleKineticLawParameter(self, request, response):

        datafile = self.getDataFile(request)
        sbmlfiles = self.getSBMLFile(request)

        if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
            message = "The data file is not tab delimited or rows contain unequal number of columns."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        mappingfile = None
        if request.get_element_MappingFile():
            mappingfile = self.getMappingFile(request)
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        results,warnings= self.executeScaleKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_ScaleKineticLawParameterText(self,ps):

        request, response = SBMLmod.soap_ScaleKineticLawParameterText(self, ps)
        return self.scaleKineticLawParameterText(request, response)

    def scaleKineticLawParameterText(self, request, response):

        files = self.getFilesAsText(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeScaleKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_ScaleKineticLawParameterBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ScaleKineticLawParameterBase64Encoded(self, ps)
        return self.scaleKineticLawParameterBase64Encoded(request, response)


    def scaleKineticLawParameterBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeScaleKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response



    def soap_ScaleKineticLawParameterGzippedBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ScaleKineticLawParameterGzippedBase64Encoded(self, ps)
        return self.scaleKineticLawParameterGzippedBase64Encoded(request, response)


    def scaleKineticLawParameterGzippedBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeScaleKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def executeScaleKineticLawParameter(self, request, sbmlfiles, datafile, mappingfile):

        if not request.get_element_ParameterId():
            message = "Please state which parameter to scale."
            raise SBMLmodFault(message, "MISSING_ELEMENT")

        mapper = DataMapper()
        warnings=[]
        datacolumn=2
        if request.get_element_DataColumnNumber():
            datacolumn=int(request.get_element_DataColumnNumber())

        batch = False
        if request.get_element_BatchMode():
            batch = request.get_element_BatchMode()

        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                message = "The there are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one model file can be submitted when batch mode is set to False"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        if mappingfile!=None:
            mapper.setup(mappingfile, datafile, datacolumn,batch=batch)

            if request.get_element_MergeMode():
                mergemode = request.get_element_MergeMode()
                result = mapper.mergeExpressionValuesMappingToSameReaction(mergemode)
            else:
                result = mapper.mergeExpressionValuesMappingToSameReaction()


            self.expr = result[0]
            self.exprId = result[1]
            warnings = result[2]

        else:

            if request.get_element_DataColumnNumber():
                datacolumn=int(request.get_element_DataColumnNumber())
                self.expr,self.exprId = mapper.setup_expr(datafile, datacolumn,batch=batch)
            else:
                self.expr,self.exprId = mapper.setup_expr(datafile,batch=batch)


        newsbmlmodels=[]
        header = self.getDataHeader(datafile,datacolumn)
        editor = ModelEditor()

        if batch:

            if len(sbmlfiles)>1:


                for i in range(len(sbmlfiles)):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                    if sbmlDocument.getNumErrors():
                        message = "The SBML file is not valid."
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                    newModel, warnings = editor.scaleKineticLawParameter(document=sbmlDocument, data=self.expr, column=i,datainfo=self.exprId,parameter=request.get_element_ParameterId(), warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlmodels.append(sbmlDocument)

            else:
                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                for i in range(len(self.expr[0])):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                    newModel, warnings = editor.scaleKineticLawParameter(document=sbmlDocument, data=self.expr, column=i,datainfo=self.exprId,parameter=request.get_element_ParameterId(), warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlmodels.append(sbmlDocument)



        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            newModel, warnings = editor.scaleKineticLawParameter(document=sbmlDocument, data=self.expr, column=0,datainfo=self.exprId,parameter=request.get_element_ParameterId(), warnings=warnings)

            sbmlDocument.setModel(newModel)
            newsbmlmodels.append(sbmlDocument)


        return [newsbmlmodels,header],warnings

    def soap_AddKineticLawParameter(self, ps):
        request, response = SBMLmod.soap_AddKineticLawParameter(self, ps)
        return self.addKineticLawParameter(request, response)
    def addKineticLawParameter(self, request, response):

        sbmlfiles = self.getSBMLFile(request)
        parameter = request.get_element_ParameterId()

        self.option = self.getOption(request)

        if not self.option:
            raise SBMLmodFault('A DefaultValue and/or a DataFile must be supplied', "MISSING_ELEMENT")

        reader = SBMLReader()

        warnings=[]
        newsbmlfiles=[]
        editor = ModelEditor()

        SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass

        if self.option=='INSERT_DEFAULT':

            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])
            newModel, warnings = editor.addKineticLawParameter(sbmlDocument, parameter,warnings, request.get_element_DefaultValue())

            sbmlDocument.setModel(newModel)
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name("NewModelWithDefault_"+parameter+"_Value")
            sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))

            newsbmlfiles.append(sbmlEditfile)

        else:
            datafile = self.getDataFile(request)
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
                message = "The data file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            if not request.get_element_DefaultValue():
                message = "A default value must be set for the parameter 'DefaultValue' for reactions that do not have an entry in the data file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


            batch = False
            if request.get_element_BatchMode():
                batch = request.get_element_BatchMode()

            datacolumn=2
            if request.get_element_DataColumnNumber():
                datacolumn=int(request.get_element_DataColumnNumber())

            if batch:
                if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                    message = "The there are more model files than number of columns in the datafile"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            else:
                if len(sbmlfiles) > 1:
                    message = "Only one model file can be submitted when batch mode is set to False"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            mapper = DataMapper()
            if self.option=='INSERT_DATA_THEN_DEFAULT':
                self.expr,self.exprId = mapper.setup_expr(expr_string=datafile, col=datacolumn, batch = batch)

            else:

                mappingfile = self.getMappingFile(request)
                if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                    message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                mapper.setup(mapping_string=mappingfile,expr_string=datafile, col=datacolumn, batch=batch)
                ret=[]
                if request.get_element_MergeMode():
                    ret = mapper.mergeExpressionValuesMappingToSameReaction(mode=request.get_element_MergeMode())
                else: ret = mapper.mergeExpressionValuesMappingToSameReaction()
                self.expr = ret[0]
                self.exprId=ret[1]
                warnings = ret[2]

            header = self.getDataHeader(datafile)

            if batch:

                if len(sbmlfiles)>1:

                    for i in range(len(sbmlfiles)):
                        reader = SBMLReader()
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        newModel, warnings = editor.addKineticLawParameter(document=sbmlDocument, parameter=parameter,warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr,column=i,datainfo=self.exprId)

                        sbmlDocument.setModel(newModel)
                        writer = SBMLWriter()
                        sbmlEditfile = SBMLmod_file()
                        sbmlEditfile.set_element_Name(header[i+datacolumn-1])
                        sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))

                        newsbmlfiles.append(sbmlEditfile)
                else:
                    reader = SBMLReader()

                    for i in range(len(self.expr[0])):
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        newModel, warnings = editor.addKineticLawParameter(document=sbmlDocument, parameter=parameter,warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr,column=i,datainfo=self.exprId)

                        sbmlDocument.setModel(newModel)
                        writer = SBMLWriter()
                        sbmlEditfile = SBMLmod_file()
                        sbmlEditfile.set_element_Name(header[i+datacolumn-2])
                        sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))

                        newsbmlfiles.append(sbmlEditfile)

            else:

                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                newModel, warnings = editor.addKineticLawParameter(document=sbmlDocument, parameter=parameter,warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr,datainfo=self.exprId)
                sbmlDocument.setModel(newModel)
                writer = SBMLWriter()
                sbmlEditfile = SBMLmod_file()

                sbmlEditfile.set_element_Name(header[datacolumn-2])
                sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))

                newsbmlfiles.append(sbmlEditfile)





        response.set_element_SbmlModelFiles(newsbmlfiles)
        response.set_element_Warnings(warnings)

        return request, response



    def soap_AddBoundsToKineticLaw(self, ps):
        request, response = SBMLmod.soap_AddBoundsToKineticLaw(self, ps)
        return self.addBoundsToKineticLaw(request, response)
    def addBoundsToKineticLaw(self, request, response):

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

        results,warnings= self.executeAddBoundsToKineticLaw(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response



    def soap_AddBoundsToKineticLawText(self,ps):

        request, response = SBMLmod.soap_AddBoundsToKineticLawText(self, ps)
        return self.addBoundsToKineticLawText(request, response)

    def addBoundsToKineticLawText(self, request, response):

        files = self.getFilesAsText(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeAddBoundsToKineticLaw(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_AddBoundsToKineticLawBase64Encoded(self,ps):
        request, response = SBMLmod.soap_AddBoundsToKineticLawBase64Encoded(self, ps)
        return self.addBoundsToKineticLawBase64Encoded(request, response)


    def addBoundsToKineticLawBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeAddBoundsToKineticLaw(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_AddBoundsToKineticLawGzippedBase64Encoded(self,ps):
        request, response = SBMLmod.soap_AddBoundsToKineticLawGzippedBase64Encoded(self, ps)
        return self.addBoundsToKineticLawGzippedBase64Encoded(request, response)


    def addBoundsToKineticLawGzippedBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeAddBoundsToKineticLaw(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response



    def executeAddBoundsToKineticLaw(self, request, sbmlfiles, datafile=None, mappingfile=None):

        #self.option = self.getOption(request)

        #if not self.option:
        #    raise SBMLmodFault('A DefaultValue and/or a DataFile must be supplied', "MISSING_ELEMENT")

        if not request.get_element_DefaultValue():
                message = "A default value must be set for the parameter 'DefaultValue' for reactions that do not have an entry in the data file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        reader = SBMLReader()

        warnings=[]
        newsbmlmodels=[]
        editor = ModelEditor()
        header=[]


        #if self.option=='INSERT_DEFAULT':
        if datafile ==None:
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])
            newModel, warnings = editor.addBounds(document=sbmlDocument,warnings=warnings, default_value=request.get_element_DefaultValue())

            sbmlDocument.setModel(newModel)
            newsbmlmodels.append(sbmlDocument)

            header.append("NewModelWithDefaultLimits")

        else:

            batch = False
            if request.get_element_BatchMode():
                batch = request.get_element_BatchMode()

            datacolumn=2
            if request.get_element_DataColumnNumber():
                datacolumn=int(request.get_element_DataColumnNumber())

            if batch:
                if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                    message = "The there are more model files than number of columns in the datafile"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            else:
                if len(sbmlfiles) > 1:
                    message = "Only one model file can be submitted when batch mode is set to False"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            mapper = DataMapper()
            if mappingfile==None:
            #if self.option=='INSERT_DATA_THEN_DEFAULT':
                self.expr,self.exprId = mapper.setup_expr(expr_string=datafile, col=datacolumn, batch = batch)

            else:
                mapper.setup(mapping_string=mappingfile,expr_string=datafile, col=datacolumn, batch=batch)
                ret=[]
                if request.get_element_MergeMode():
                    ret = mapper.mergeExpressionValuesMappingToSameReaction(request.get_element_MergeMode())
                else: ret = mapper.mergeExpressionValuesMappingToSameReaction()
                self.expr = ret[0]
                self.exprId=ret[1]
                warnings = ret[2]

            header = self.getDataHeader(datafile,datacolumn)

            if batch:

                if len(sbmlfiles)>1:
                    for i in range(len(sbmlfiles)):
                        reader = SBMLReader()
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        newModel, warnings = editor.addBounds(document=sbmlDocument,warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr,column=i,datainfo=self.exprId)

                        sbmlDocument.setModel(newModel)
                        newsbmlmodels.append(sbmlDocument)
                else:
                    reader = SBMLReader()

                    for i in range(len(self.expr[0])):
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        newModel, warnings = editor.addBounds(document=sbmlDocument,warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr,column=i,datainfo=self.exprId)

                        sbmlDocument.setModel(newModel)
                        newsbmlmodels.append(sbmlDocument)

            else:

                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                newModel, warnings = editor.addBounds(document=sbmlDocument,warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr,datainfo=self.exprId)

                sbmlDocument.setModel(newModel)
                newsbmlmodels.append(sbmlDocument)


        return [newsbmlmodels,header],warnings

    def soap_ReplaceInitialConcentrationsOfSpecies(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpecies(self, ps)
        return self.replaceInitialConcentrationsOfSpecies(request, response)
    def replaceInitialConcentrationsOfSpecies(self, request, response):
        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceInitialConcentrationsOfSpecies(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceInitialConcentrationsOfSpeciesText(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpeciesText(self, ps)
        return self.replaceInitialConcentrationsOfSpeciesText(request, response)

    def replaceInitialConcentrationsOfSpeciesText(self, request, response):
        files = self.getFilesText(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceInitialConcentrationsOfSpecies(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_ReplaceInitialConcentrationsOfSpeciesBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpeciesBase64Encoded(self, ps)
        return self.replaceInitialConcentrationsOfSpeciesBase64Encoded(request, response)

    def replaceInitialConcentrationsOfSpeciesBase64Encoded(self, request, response):
        files = self.getFilesDecodeBase64(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceInitialConcentrationsOfSpecies(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(self, ps):
        request, response = SBMLmod.soap_ReplaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(self, ps)
        return self.replaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(request, response)

    def replaceInitialConcentrationsOfSpeciesGzippedBase64Encoded(self, request, response):
        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceInitialConcentrationsOfSpecies(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response



    def executeReplaceInitialConcentrationsOfSpecies(self, request, sbmlfiles, datafile, mappingfile=None):
        mapper = DataMapper()
        warnings=[]
        datacolumn=2

        if request.get_element_DataColumnNumber():
            datacolumn=int(request.get_element_DataColumnNumber())

        batch=False
        if request.get_element_BatchMode():
            batch=request.get_element_BatchMode()

        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                message = "The there are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        if mappingfile:

            mapper.setup(mappingfile, datafile, col=datacolumn,batch=batch)
            result = mapper.mergeExpressionValuesMappingToSameReaction()

            self.conc = result[0]
            self.metId = result[1]
            warnings = result[2]

        else:
            self.conc, self.metId = mapper.setup_expr(datafile, col=datacolumn,batch=batch)


        newsbmlfiles=[]
        header = self.getDataHeader(datafile,datacolumn)
        editor = ModelEditor()

        reader = SBMLReader()
        for i in range(len(sbmlfiles)):

            sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            if batch:
                newModel, warnings = editor.editInitialConcentrations(document=sbmlDocument, data = self.conc, datainfo=self.metId,warnings=warnings, column=i)
            else:
                newModel, warnings = editor.editInitialConcentrations(document=sbmlDocument, data = self.conc, datainfo=self.metId,warnings=warnings, column=datacolumn-2)

            sbmlDocument.setModel(newModel)

            newsbmlfiles.append(sbmlDocument)

        return [newsbmlfiles,header],warnings

    def soap_ReplaceGlobalParameters(self, ps):
        request, response = SBMLmod.soap_ReplaceGlobalParameters(self, ps)
        return self.replaceGlobalParameters(request, response)

    def replaceGlobalParameters(self, request, response):

        sbmlfiles = self.getSBMLFile(request)
        datafile = self.getDataFile(request)

        if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(datafile):
            message = "The data file is not tab delimited or rows contain unequal number of columns."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        if request.get_element_MappingFile():
            mappingfile = self.getMappingFile(request)
            if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        results,warnings= self.executeReplaceGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response


    def soap_ReplaceGlobalParametersText(self,ps):
        request, response = SBMLmod.soap_ReplaceGlobalParametersText(self,ps)
        return self.replaceGlobalParametersText(request,response)

    def replaceGlobalParametersText(self,request, response):

        files = self.getFilesAsText(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceGlobalParametersBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ReplaceGlobalParametersBase64Encoded(self, ps)
        return self.replaceGlobalParametersBase64Encoded(request, response)


    def replaceGlobalParametersBase64Encoded(self, request, response):
        files = self.getFilesDecodeBase64(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ReplaceGlobalParametersGzippedBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ReplaceGlobalParametersGzippedBase64Encoded(self, ps)
        return self.replaceGlobalParametersGzippedBase64Encoded(request, response)


    def replaceGlobalParametersGzippedBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeReplaceGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response



    def executeReplaceGlobalParameters(self,request, sbmlfiles, datafile, mappingfile):


        mapper = DataMapper()
        warnings=[]

        datacolumn=2

        if request.get_element_DataColumnNumber():
            datacolumn=int(request.get_element_DataColumnNumber())

        batch = request.get_element_BatchMode()

        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                message = "The there are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one file can be submitted when batch mode is set to False"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        if mappingfile != None:
            mapper.setup(mappingfile, datafile, datacolumn,batch=batch)
            if request.get_element_MergeMode():
                mergemode = request.get_element_MergeMode()
                result = mapper.mergeExpressionValuesMappingToSameReaction(mode=mergemode)
            else:

                result = mapper.mergeExpressionValuesMappingToSameReaction()


            self.expr = result[0]
            self.exprId = result[1]
            warnings = result[2]

        else:
            self.expr, self.exprId = mapper.setup_expr(datafile, datacolumn,batch=batch)


        #SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass

        newsbmlfiles=[]
        header = self.getDataHeader(datafile,datacolumn)
        editor = ModelEditor()

        if batch:
            if len(sbmlfiles)>1:


                for i in range(len(sbmlfiles)):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                    if sbmlDocument.getNumErrors():
                        message = "The SBML file is not valid."
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                    newModel, warnings = editor.replaceGlobalParameters(document=sbmlDocument, data=self.expr,column=i,datainfo=self.exprId, warnings=warnings)

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

                    newModel, warnings = editor.replaceGlobalParameters(document=sbmlDocument, data=self.expr,column=i,datainfo=self.exprId, warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlfiles.append(sbmlDocument)



        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            newModel, warnings = editor.replaceGlobalParameters(document=sbmlDocument, data=self.expr,column=0,datainfo=self.exprId, warnings=warnings)

            sbmlDocument.setModel(newModel)
            newsbmlfiles.append(sbmlDocument)


        return [newsbmlfiles,header],warnings

    def soap_ScaleGlobalParametersText(self,ps):
        request, response = SBMLmod.soap_ScaleGlobalParametersText(self,ps)
        return self.scaleGlobalParametersText(request,response)

    def scaleGlobalParametersText(self,request, response):

        files = self.getFilesAsText(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeScaleGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileText(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ScaleGlobalParametersBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ScaleGlobalParametersBase64Encoded(self, ps)
        return self.scaleGlobalParametersBase64Encoded(request, response)


    def scaleGlobalParametersBase64Encoded(self, request, response):
        files = self.getFilesDecodeBase64(request)
        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeScaleGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def soap_ScaleGlobalParametersGzippedBase64Encoded(self,ps):
        request, response = SBMLmod.soap_ScaleGlobalParametersGzippedBase64Encoded(self, ps)
        return self.scaleGlobalParametersGzippedBase64Encoded(request, response)


    def scaleGlobalParametersGzippedBase64Encoded(self, request, response):

        files = self.getFilesDecodeBase64Gunzip(request)

        sbmlfiles=files[0]
        datafile=files[1]
        mappingfile=files[2]

        results,warnings= self.executeScaleGlobalParameters(request, sbmlfiles, datafile, mappingfile)

        response.set_element_SbmlModelFiles(self.writeResultsToFileGzippedBase64Encoded(results))
        response.set_element_Warnings(warnings)

        return request, response

    def executeScaleGlobalParameters(self,request, sbmlfiles, datafile, mappingfile):

        mapper = DataMapper()
        warnings=[]

        datacolumn=2

        if request.get_element_DataColumnNumber():
            datacolumn=int(request.get_element_DataColumnNumber())

        batch = request.get_element_BatchMode()

        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile)-datacolumn+1:
                message = "The there are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one file can be submitted when batch mode is set to False"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        if mappingfile != None:
            mapper.setup(mappingfile, datafile, datacolumn,batch=batch)
            if request.get_element_MergeMode():
                mergemode = request.get_element_MergeMode()
                result = mapper.mergeExpressionValuesMappingToSameReaction(mode=mergemode)
            else:

                result = mapper.mergeExpressionValuesMappingToSameReaction()

            self.expr = result[0]
            self.exprId = result[1]
            warnings = result[2]

        else:
            self.expr, self.exprId = mapper.setup_expr(datafile, datacolumn,batch=batch)


        #SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass

        newsbmlfiles=[]
        header = self.getDataHeader(datafile,datacolumn)
        editor = ModelEditor()

        if batch:

            if len(sbmlfiles)>1:


                for i in range(len(sbmlfiles)):
                    reader = SBMLReader()
                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                    if sbmlDocument.getNumErrors():
                        message = "The SBML file is not valid."
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                    newModel, warnings = editor.scaleGlobalParameters(document=sbmlDocument, data=self.expr,column=i,datainfo=self.exprId, warnings=warnings)

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

                    newModel, warnings = editor.scaleGlobalParameters(document=sbmlDocument, data=self.expr,column=i,datainfo=self.exprId, warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlfiles.append(sbmlDocument)



        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            newModel, warnings = editor.scaleGlobalParameters(document=sbmlDocument, data=self.expr,column=0,datainfo=self.exprId, warnings=warnings)

            sbmlDocument.setModel(newModel)
            newsbmlfiles.append(sbmlDocument)


        return [newsbmlfiles,header],warnings


    def getMappingFile(self, request):
        try:
            mappingfile = zlib.decompress(base64.b64decode(request.get_element_MappingFile())).strip()
        except:
            message = "The mapping file could not be decompressed, ensure file is not emtpy, zipped and then encoded as a string."
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        return mappingfile

    def getSBMLFile(self, request):
        sbmlfiles=[]

        files = request.get_element_SbmlModelFiles()

        for file in files:
            try:
                sbmlfiles.append( zlib.decompress(base64.b64decode(file)).strip())
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

    def isTabDelimitedAndAllRowsContainEqualNumberOfColumns(self,datafile):
        lines = datafile.split('\n')

        firstcolno = 0
        first = True

        for i in range(1,len(lines)):
            line = lines[i]
            if not first:
                colno = line.count('\t')

                if colno==0:
                    return False
                if colno != firstcolno:
                    return False
            else:
                firstcolno=line.count('\t')
                if firstcolno==0:
                    return False
                first=False
        return True

    def getDataHeader(self,datafile,col=2):
        line = datafile.split('\n')[0]
        columns = line.split('\t')
        header=[]

        for i in range(col-1,len(columns)):
            header.append(columns[i])

        return header

    def getNumberOfColumnsInDataFile(self,datafile):
        line = datafile.split('\n')[0]

        return line.count('\t')+1

    def getOption(self, request):
        option1='INSERT_DEFAULT'
        option2='INSERT_DATA_THEN_DEFAULT'
        option3='INSERT_DATA_WITH_MAPPING_THEN_DEFAULT'
        option=None

        if request.get_element_DataFile():
            if request.get_element_MappingFile():
                option=option3
            else:
                option=option2

        elif request.get_element_DefaultValue():
            option=option1

        return option


    def writeResultsToFileGzippedBase64Encoded(self,results):

        SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass
        sbmlDocuments = results[0]
        header = results[1]

        writtenFiles=[]

        for i in range(len(sbmlDocuments)):
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name(header[i])
            sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocuments[i]))))
            writtenFiles.append(sbmlEditfile)

        return writtenFiles

    def writeResultsToFileBase64Encoded(self,results):

        SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass
        sbmlDocuments = results[0]
        header = results[1]

        writtenFiles=[]

        for i in range(len(sbmlDocuments)):
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name(header[i])
            sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(writer.writeSBMLToString(sbmlDocuments[i])))
            writtenFiles.append(sbmlEditfile)

        return writtenFiles

    def writeResultsToFileText(self,results):
        SBMLmod_file=SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod","SbmlModelFilesType")).pyclass
        sbmlDocuments = results[0]
        header = results[1]

        writtenFiles=[]

        for i in range(len(sbmlDocuments)):
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name(header[i])
            sbmlEditfile.set_element_SbmlModelFile(writer.writeSBMLToString(sbmlDocuments[i]))
            writtenFiles.append(sbmlEditfile)


        return writtenFiles


def main():
    port = 8080
    address = ('', port)
    sc = ServiceContainer.ServiceContainer(address, [SBMLmodWS()])
    sc.serve_forever()

if __name__ == '__main__':
    main()
