'''
Created on Jul 3, 2015

@author: schaeuble
'''
import base64, zlib

from libsbml import SBMLReader, SBMLWriter
from sbmlmod.DataMapper import DataMapper
from sbmlmod.ModelEditor import ModelEditor
from sbmlmod.SBMLmod_fault import SBMLmodFault
from sbmlmod.SBMLmod_types import ns0 as SBMLfiletypeNs

class ManipulateKineticParameters(object):
    '''
    classdocs
    '''

    

    def replaceKineticLawParameter(self, request, files):        
        sbmlfiles = files[0]
        datafile = files[1]
        mappingfile = files[2]

        results, warnings = self.executeReplaceKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        return results, warnings
    
    def scaleKineticLawParameter(self, request, files):        
        sbmlfiles = files[0]
        datafile = files[1]
        mappingfile = files[2]

        results, warnings = self.executeScaleKineticLawParameter(request, sbmlfiles, datafile, mappingfile)

        return results, warnings

    def addBoundsToKineticLaw(self, request, files):        
        sbmlfiles = files[0]
        datafile = files[1]
        mappingfile = files[2]

        results, warnings = self.executeAddBoundsToKineticLaw(request, sbmlfiles, datafile, mappingfile)

        return results, warnings    


    def executeReplaceKineticLawParameter(self, request, sbmlfiles, datafile, mappingfile):
        if not request.get_element_ParameterId():
            message = "Please state which parameter to scale."
            raise SBMLmodFault(message, "MISSING_ELEMENT")

        mapper = DataMapper()
        warnings = []

        datacolumn = 2
        if request.get_element_DataColumnNumber():
            datacolumn = int(request.get_element_DataColumnNumber())

        batch = False
        if request.get_element_BatchMode():
            batch = request.get_element_BatchMode()


        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile) - datacolumn + 1:
                message = "There are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one model file can be submitted when batch mode is set to False"
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
            if request.get_element_DataColumnNumber():
                datacolumn = int(request.get_element_DataColumnNumber())
                self.expr, self.exprId = mapper.setup_expr(datafile, datacolumn, batch=batch)
            else:
                self.expr, self.exprId = mapper.setup_expr(datafile, batch=batch)

        newmodels = []
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
                    
                    for j in range(len(self.expr[0])):
                        newModel, warnings = editor.replaceKineticLawParameter(document=sbmlDocument, data=self.expr, column=j, datainfo=self.exprId, parameter=request.get_element_ParameterId(), warnings=warnings)

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

                    newModel, warnings = editor.replaceKineticLawParameter(document=sbmlDocument, data=self.expr, column=i, datainfo=self.exprId, parameter=request.get_element_ParameterId(), warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newmodels.append(sbmlDocument)

        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            newModel, warnings = editor.replaceKineticLawParameter(document=sbmlDocument, data=self.expr, column=0, datainfo=self.exprId, parameter=request.get_element_ParameterId(), warnings=warnings)

            sbmlDocument.setModel(newModel)
            newmodels.append(sbmlDocument)

        return [newmodels, header], warnings

        
    def executeScaleKineticLawParameter(self, request, sbmlfiles, datafile, mappingfile):

        if not request.get_element_ParameterId():
            message = "Please state which parameter to scale."
            raise SBMLmodFault(message, "MISSING_ELEMENT")

        mapper = DataMapper()
        warnings = []
        datacolumn = 2
        if request.get_element_DataColumnNumber():
            datacolumn = int(request.get_element_DataColumnNumber())

        batch = False
        if request.get_element_BatchMode():
            batch = request.get_element_BatchMode()


        if batch:
            if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile) - datacolumn + 1:
                message = "There are more model files than number of columns in the datafile"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
        else:
            if len(sbmlfiles) > 1:
                message = "Only one model file can be submitted when batch mode is set to False"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")


        if mappingfile != None:
            mapper.setup(mappingfile, datafile, datacolumn, batch=batch)

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
                datacolumn = int(request.get_element_DataColumnNumber())
                self.expr, self.exprId = mapper.setup_expr(datafile, datacolumn, batch=batch)
            else:
                self.expr, self.exprId = mapper.setup_expr(datafile, batch=batch)


        newsbmlmodels = []
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
                    
                    for j in range(len(self.expr[0])):
                        newModel, warnings = editor.scaleKineticLawParameter(document=sbmlDocument, data=self.expr, column=j, datainfo=self.exprId, parameter=request.get_element_ParameterId(), warnings=warnings)
    
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

                    newModel, warnings = editor.scaleKineticLawParameter(document=sbmlDocument, data=self.expr, column=i, datainfo=self.exprId, parameter=request.get_element_ParameterId(), warnings=warnings)

                    sbmlDocument.setModel(newModel)
                    newsbmlmodels.append(sbmlDocument)

        else:
            reader = SBMLReader()
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

            if sbmlDocument.getNumErrors():
                message = "The SBML file is not valid."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            newModel, warnings = editor.scaleKineticLawParameter(document=sbmlDocument, data=self.expr, column=0, datainfo=self.exprId, parameter=request.get_element_ParameterId(), warnings=warnings)

            sbmlDocument.setModel(newModel)
            newsbmlmodels.append(sbmlDocument)

        return [newsbmlmodels, header], warnings


    
    def executeAddBoundsToKineticLaw(self, request, sbmlfiles, datafile=None, mappingfile=None):

        # self.option = self.getOption(request)

        # if not self.option:
        #    raise SBMLmodFault('A DefaultValue and/or a DataFile must be supplied', "MISSING_ELEMENT")

        if not request.get_element_DefaultValue():
                message = "A default value must be set for the parameter 'DefaultValue' for reactions that do not have an entry in the data file"
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        reader = SBMLReader()

        warnings = []
        newsbmlmodels = []
        editor = ModelEditor()
        header = []


        # if self.option=='INSERT_DEFAULT':
        if datafile == None:
            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])
            newModel, warnings = editor.addBounds(document=sbmlDocument, warnings=warnings, default_value=request.get_element_DefaultValue())

            sbmlDocument.setModel(newModel)
            newsbmlmodels.append(sbmlDocument)

            header.append("NewModelWithDefaultLimits")

        else:

            batch = False
            if request.get_element_BatchMode():
                batch = request.get_element_BatchMode()

            datacolumn = 2
            if request.get_element_DataColumnNumber():
                datacolumn = int(request.get_element_DataColumnNumber())

            if batch:
                if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile) - datacolumn + 1:
                    message = "The there are more model files than number of columns in the datafile"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            else:
                if len(sbmlfiles) > 1:
                    message = "Only one model file can be submitted when batch mode is set to False"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            mapper = DataMapper()
            if mappingfile == None:
            # if self.option=='INSERT_DATA_THEN_DEFAULT':
                self.expr, self.exprId = mapper.setup_expr(expr_string=datafile, col=datacolumn, batch=batch)

            else:
                mapper.setup(mapping_string=mappingfile, expr_string=datafile, col=datacolumn, batch=batch)
                ret = []
                if request.get_element_MergeMode():
                    ret = mapper.mergeExpressionValuesMappingToSameReaction(request.get_element_MergeMode())
                else: ret = mapper.mergeExpressionValuesMappingToSameReaction()
                self.expr = ret[0]
                self.exprId = ret[1]
                warnings = ret[2]

            header = self.getDataHeader(datafile, datacolumn)

            if batch:

                if len(sbmlfiles) > 1:
                    for i in range(len(sbmlfiles)):
                        reader = SBMLReader()
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        for j in range(len(self.expr[0])):
                            newModel, warnings = editor.addBounds(document=sbmlDocument, warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr, column=j, datainfo=self.exprId)
    
                            sbmlDocument.setModel(newModel)
                            newsbmlmodels.append(sbmlDocument)
                
                else:
                    reader = SBMLReader()

                    sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])
                    for i in range(len(self.expr[0])):

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        newModel, warnings = editor.addBounds(document=sbmlDocument, warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr, column=i, datainfo=self.exprId)

                        sbmlDocument.setModel(newModel)
                        newsbmlmodels.append(sbmlDocument)

            else:
                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                newModel, warnings = editor.addBounds(document=sbmlDocument, warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr, datainfo=self.exprId)

                sbmlDocument.setModel(newModel)
                newsbmlmodels.append(sbmlDocument)

        return [newsbmlmodels, header], warnings    
    
    
    def addKineticLawParameter(self, request, response):

        sbmlfiles = self.getSBMLFile(request)
        parameter = request.get_element_ParameterId()

        self.option = self.getOption(request)

        if not self.option:
            raise SBMLmodFault('A DefaultValue and/or a DataFile must be supplied', "MISSING_ELEMENT")

        reader = SBMLReader()

        warnings = []
        newsbmlfiles = []
        editor = ModelEditor()

        SBMLmod_file = SBMLfiletypeNs.SbmlModelFilesType_Def(("http://esysbio.org/service/bio/SBMLmod", "SbmlModelFilesType")).pyclass

        if self.option == 'INSERT_DEFAULT':

            sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])
            newModel, warnings = editor.addKineticLawParameter(sbmlDocument, parameter, warnings, request.get_element_DefaultValue())

            sbmlDocument.setModel(newModel)
            writer = SBMLWriter()
            sbmlEditfile = SBMLmod_file()
            sbmlEditfile.set_element_Name("NewModelWithDefault_" + parameter + "_Value")
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

            datacolumn = 2
            if request.get_element_DataColumnNumber():
                datacolumn = int(request.get_element_DataColumnNumber())

            if batch:
                if len(sbmlfiles) > self.getNumberOfColumnsInDataFile(datafile) - datacolumn + 1:
                    message = "The there are more model files than number of columns in the datafile"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
            else:
                if len(sbmlfiles) > 1:
                    message = "Only one model file can be submitted when batch mode is set to False"
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            mapper = DataMapper()
            if self.option == 'INSERT_DATA_THEN_DEFAULT':
                self.expr, self.exprId = mapper.setup_expr(expr_string=datafile, col=datacolumn, batch=batch)

            else:

                mappingfile = self.getMappingFile(request)
                if not self.isTabDelimitedAndAllRowsContainEqualNumberOfColumns(mappingfile):
                    message = "The mapping file is not tab delimited or rows contain unequal number of columns."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                mapper.setup(mapping_string=mappingfile, expr_string=datafile, col=datacolumn, batch=batch)
                ret = []
                if request.get_element_MergeMode():
                    ret = mapper.mergeExpressionValuesMappingToSameReaction(mode=request.get_element_MergeMode())
                else: ret = mapper.mergeExpressionValuesMappingToSameReaction()
                self.expr = ret[0]
                self.exprId = ret[1]
                warnings = ret[2]

            header = self.getDataHeader(datafile)

            if batch:

                if len(sbmlfiles) > 1:

                    for i in range(len(sbmlfiles)):
                        reader = SBMLReader()
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[i])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        for j in range(len(self.expr[0])):
                            newModel, warnings = editor.addKineticLawParameter(document=sbmlDocument, parameter=parameter, warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr, column=j, datainfo=self.exprId)
    
                            sbmlDocument.setModel(newModel)
                            writer = SBMLWriter()
                            sbmlEditfile = SBMLmod_file()
                            sbmlEditfile.set_element_Name(header[j + datacolumn - 1])
                            sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))
    
                            newsbmlfiles.append(sbmlEditfile)
                else:
                    reader = SBMLReader()

                    for i in range(len(self.expr[0])):
                        sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                        if sbmlDocument.getNumErrors():
                            message = "The SBML file is not valid."
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                        newModel, warnings = editor.addKineticLawParameter(document=sbmlDocument, parameter=parameter, warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr, column=i, datainfo=self.exprId)

                        sbmlDocument.setModel(newModel)
                        writer = SBMLWriter()
                        sbmlEditfile = SBMLmod_file()
                        sbmlEditfile.set_element_Name(header[i + datacolumn - 2])
                        sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))

                        newsbmlfiles.append(sbmlEditfile)

            else:
                reader = SBMLReader()
                sbmlDocument = reader.readSBMLFromString(sbmlfiles[0])

                if sbmlDocument.getNumErrors():
                    message = "The SBML file is not valid."
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                newModel, warnings = editor.addKineticLawParameter(document=sbmlDocument, parameter=parameter, warnings=warnings, default_value=request.get_element_DefaultValue(), data=self.expr, datainfo=self.exprId)
                sbmlDocument.setModel(newModel)
                writer = SBMLWriter()
                sbmlEditfile = SBMLmod_file()

                sbmlEditfile.set_element_Name(header[datacolumn - 2])
                sbmlEditfile.set_element_SbmlModelFile(base64.b64encode(zlib.compress(writer.writeSBMLToString(sbmlDocument))))

                newsbmlfiles.append(sbmlEditfile)

        response.set_element_SbmlModelFiles(newsbmlfiles)
        response.set_element_Warnings(warnings)

        return request, response    
    
    def getNumberOfColumnsInDataFile(self, datafile):
        line = datafile.split('\n')[0]
        return line.count('\t') + 1
    
