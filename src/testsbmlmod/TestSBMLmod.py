import unittest
import base64
import zlib
from sbmlmod.SBMLmod_server import ValidateSBMLModelRequest,\
    ValidateSBMLModelResponse, ReplaceKineticLawParameterRequest,\
    ReplaceKineticLawParameterResponse, ScaleKineticLawParameterRequest,\
    ScaleKineticLawParameterResponse,\
    ReplaceInitialConcentrationsOfSpeciesRequest,\
    ReplaceInitialConcentrationsOfSpeciesResponse,\
    AddKineticLawParameterRequest, AddKineticLawParameterResponse,\
    AddBoundsToKineticLawRequest, AddBoundsToKineticLawResponse
from sbmlmod.SBMLmod import SBMLmodWS
from sbmlmod.SBMLmod_fault import SBMLmodFault
from libsbml import SBMLReader
from sbmlmod.facades import version_facade

class TestSBMLmod(unittest.TestCase):


    def setUp(self):
        self.impl = SBMLmodWS()
    def testValidateModelGzippedBase64EncodedGivesException(self):
        request = ValidateSBMLModelRequest()
        response = ValidateSBMLModelResponse()
        sbmlfile_lines = open('resources/ValidSBML.xml','r').readlines()
        sbmlfile = "".join(sbmlfile_lines)
        requestfile = base64.b64encode(sbmlfile)

        request.set_element_SbmlModelFile(requestfile)
        self.assertRaises(SBMLmodFault, self.impl.validateSBMLModelGzippedBase64Encoded,request, response)



    def testFileNotCompressedGivenToValidateSBMLModelGivesException(self):
        request, response = self.validateSBMLModelCommonSetup()
        sbmlfile_lines = open('resources/ValidSBML.xml','r').readlines()
        sbmlfile = "".join(sbmlfile_lines)

        request.set_element_SbmlModelFile(sbmlfile)
        self.assertRaises(SBMLmodFault, self.impl.validateSBMLModel, request, response)
        try:
            request, response = self.impl.validateSBMLModel(request, response)
        except SBMLmodFault as e:
            self.assertEquals("FILE_HANDLING_ERROR", e.faultEnum)

    def testWrongFileAsInputToValidateSBMLModelTriggersNotValidModelResponse(self):
        request, response = self.validateSBMLModelCommonSetup()
        sbmlfile_lines = open('resources/mapping.txt','r').readlines()
        sbmlfile = "".join(sbmlfile_lines)

        request.set_element_SbmlModelFile(base64.b64encode(zlib.compress(sbmlfile)))
        request, response = self.impl.validateSBMLModel(request, response)
        self.assertFalse(response.get_element_ModelIsValid())
        self.assertEquals(3, len(response.get_element_ErrorMessages()))

    def validateSBMLModelCommonSetup(self):
        request = ValidateSBMLModelRequest()
        response = ValidateSBMLModelResponse()
        return request, response



    def testSBMLFileNotCompressedCorrectlyToReplaceKineticLawParameterRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([filelines])

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter,request, response)

    def testDataFileNotCompressedCorrectlyToReplaceKineticLawParameterRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TestingAvGenuttryksformater.csv', 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter,request, response)

    def testMappingFileNotCompressedCorrectlyToReplaceKineticLawParameterRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_MappingFile(zlib.compress(filelines))

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter,request, response)

    def testFileEmptyRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request.set_element_DataFile("")

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testReplaceKineticLawParameterWorksInBestCase(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request, response = self.impl.replaceKineticLawParameter(request, response)

        file = response.get_element_SbmlModelFiles()[0].SbmlModelFile
        sbmlfile=zlib.decompress(base64.b64decode(file))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmlfile)

        self.assertEquals(472.65,sbmlDocument.getModel().getReaction('R02174').getKineticLaw().getParameter('E_T').getValue())


    def testReplaceKineticLawParameterBatchModeReturnsCorrectNumberOfFiles (self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request.set_element_BatchMode(True)
        request.set_element_DataColumnNumber(3)
        request, response = self.impl.replaceKineticLawParameter(request, response)


        sbmlfiles = response.get_element_SbmlModelFiles()

        self.assertEquals(4,len(sbmlfiles))




    def testReplaceKineticLawParameterReturnsWarnings(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request, response = self.impl.replaceKineticLawParameter(request, response)
        warnings = response.get_element_Warnings()
        self.assertTrue(warnings)

    def testFileHandlingErrorThrownFromReplaceKineticLawParameterWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TestingAvGenuttryksformater_commaSeparated.csv', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def replaceKineticLawParameterCommonSetup(self):
        request = ReplaceKineticLawParameterRequest()
        response = ReplaceKineticLawParameterResponse()
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/TestingAvGenuttryksformater.csv', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        sbml=[base64.b64encode(zlib.compress(filelines))]
        request.set_element_SbmlModelFiles(sbml)
        request.set_element_ParameterId("E_T")
        request.set_element_DataColumnNumber(2)
        return request, response


    def testSBMLFileNotCompressedCorrectlyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([filelines])

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testDataFileNotCompressedCorrectlyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TestingAvGenuttryksformater.csv', 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter,request, response)

    def testMappingFileNotCompressedCorrectlyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_MappingFile(zlib.compress(filelines))

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter,request, response)

    def testFileEmptyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        request.set_element_DataFile("")

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)

    def testFileHandlingErrorThrownFromScaleKineticLawParameterWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TestingAvGenuttryksformater_commaSeparated.csv', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testScaleKineticLawParameterWorksInBestCase(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        request, response = self.impl.scaleKineticLawParameter(request, response)

        file = response.get_element_SbmlModelFiles()[0]
        sbmlfile=zlib.decompress(base64.b64decode(file.SbmlModelFile))

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmlfile)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())


    def testScaleKineticLawParameterReturnsWarnings(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        request, response = self.impl.scaleKineticLawParameter(request, response)
        warnings = response.get_element_Warnings()
        self.assertTrue(warnings)

    def testScaleKineticLawParameterBatchModeReturnsCorrectNumberOfFiles (self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        request.set_element_BatchMode(True)
        request.set_element_DataColumnNumber(3)
        request, response = self.impl.scaleKineticLawParameter(request, response)


        sbmlfiles = response.get_element_SbmlModelFiles()

        self.assertEquals(4,len(sbmlfiles))


    def scaleKineticLawParameterCommonSetup(self):
        request = ScaleKineticLawParameterRequest()
        response = ScaleKineticLawParameterResponse()
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/TestingAvGenuttryksformater.csv', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_ParameterId("E_T")
        request.set_element_DataColumnNumber(2)
        request.set_element_MergeMode('MIN')
        return request, response

    def testSBMLFileNotCompressedCorrectlyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([filelines])

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)

    def testDataFileNotCompressedCorrectlyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/expression_glu_ace_Oh_etal.dat', 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter,request, response)

    def testMappingFileNotCompressedCorrectlyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/mapping.txt', 'r'))
        request.set_element_MappingFile(zlib.compress(filelines))

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter,request, response)

    def testFileEmptyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        request.set_element_SbmlModelFiles([""])

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)

    def testFileHandlingErrorThrownFromAddKineticLawParameterWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/TestingAvGenuttryksformater_commaSeparated.csv', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testAddKineticLawParameterUsingDefaultOnly(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()

        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DefaultValue(1000)
        request.set_element_ParameterId('UPPER')

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)


        self.assertEquals(1000,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        self.assertEquals(1000,sbmlDocument.getModel().getReaction('SYN').getKineticLaw().getParameter('UPPER').getValue())


        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())

    def testAddKineticLawParameterUsingDataOnlyWithoutMapping(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()

        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open('resources/EnzymeIdAsKey.dat', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request.set_element_ParameterId('UPPER')
        request.set_element_DefaultValue(1000)


        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))
        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        #self.assertTrue(sbmlDocument.getModel().getReaction('SYN').getKineticLaw())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmlfiles[0].SbmlModelFile)
        request, response = self.impl.validateSBMLModel(request, response)
        self.assertTrue(response.get_element_ModelIsValid())

    def testAddKineticLawParameterUsingDataAndDefaultWithoutMapping(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()

        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open('resources/EnzymeIdAsKey.dat', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request.set_element_ParameterId('UPPER')
        request.set_element_DefaultValue(1000)

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))
        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        self.assertEquals(1000,sbmlDocument.getModel().getReaction('SYN').getKineticLaw().getParameter('UPPER').getValue())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())

    def testAddKineticLawParameterUsingDataOnlyWithMapping(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()
        filelines = "".join(open('resources/mapping.txt', 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/expression_glu_ace_Oh_etal.dat', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DataColumnNumber(3)
        request.set_element_ParameterId('UPPER')
        request.set_element_DefaultValue(1000)


        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))
        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        #self.assertFalse(sbmlDocument.getModel().getReaction('SYN').getKineticLaw())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())

    def testAddKineticLawParameterUsingDataAndDefaultWithMapping(self):
        request, response = self.addKineticLawParameterCommonSetup()

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))
        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        self.assertEquals(1000,sbmlDocument.getModel().getReaction('SYN').getKineticLaw().getParameter('UPPER').getValue())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())

    def testAddKineticLawParameterBatchModeReturnsCorrectNumberOfFiles (self):
        request, response = self.addKineticLawParameterCommonSetup()
        request.set_element_BatchMode(True)
        request.set_element_DataColumnNumber(3)
        request, response = self.impl.addKineticLawParameter(request, response)


        sbmlfiles = response.get_element_SbmlModelFiles()

        self.assertEquals(3,len(sbmlfiles))



    def testAddKineticLawParameterReturnsRaisesFaultWhenWrongMappingFileIsUsed(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))

      #  request, response = self.impl.addKineticLawParameter(request, response)
     #   warnings = response.get_element_Warnings()
      #  self.assertTrue("Checking Mapping" in "".join(warnings))
        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def addKineticLawParameterCommonSetup(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()
        filelines = "".join(open('resources/mapping.txt', 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/expression_glu_ace_Oh_etal.dat', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DataColumnNumber(3)
        request.set_element_DefaultValue(1000)
        request.set_element_MergeMode("MIN")
        request.set_element_ParameterId('UPPER')
        return request, response



    def testSBMLFileNotCompressedCorrectlyToReplaceInitialConcentrationsOfSpeciesRaisesException(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([filelines])
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.replaceInitialConcentrationsOfSpecies, request, response)

    def testMappingFileNotCompressedCorrectlyToReplaceInitialConcentrationsOfSpeciesRaisesException(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open('resources/mapping_applied_rat.txt', 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.replaceInitialConcentrationsOfSpecies, request, response)

    def testFileHandlingErrorThrownFromReplaceInitialConcentrationsWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open('resources/InitialConc_acetateCommaSeparated.txt', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)

    def testReplaceInitialConcentrationsOfSpeciesWorksInBestCase(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open('resources/InitialConc_acetate.txt', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request, response = self.impl.replaceInitialConcentrationsOfSpecies(request, response)
        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))
        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())

    def testReplaceInitialConcentrationsOfSpeciesReturnsWarnings(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open('resources/TRPcatabolism.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open('resources/InitialConc_acetate.txt', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request, response = self.impl.replaceInitialConcentrationsOfSpecies(request, response)
        warnings = response.get_element_Warnings()
        self.assertTrue(warnings)


    def addBoundsCommonSetup(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()
        filelines = "".join(open('resources/mapping.txt', 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/expression_glu_ace_Oh_etal.dat', 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DataColumnNumber(3)
        request.set_element_DefaultValue(1000)

        return request, response

    def testAddDefaultBoundsToKineticLawParameter(self):
        request = AddBoundsToKineticLawRequest()
        response = AddBoundsToKineticLawResponse()

        filelines = "".join(open('resources/SBMLwithoutKinetics.xml', 'r'))
        sbml=base64.b64encode(zlib.compress(filelines))
        request.set_element_SbmlModelFiles([sbml])
        request.set_element_DefaultValue(1000)

        request, response = self.impl.addBoundsToKineticLaw(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))
        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(1000,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER_BOUND').getValue())
        self.assertEquals(0.0,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('LOWER_BOUND').getValue())

        self.assertEquals(1000,sbmlDocument.getModel().getReaction('ACN').getKineticLaw().getParameter('UPPER_BOUND').getValue())
        self.assertEquals(-1000,sbmlDocument.getModel().getReaction('ACN').getKineticLaw().getParameter('LOWER_BOUND').getValue())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())


    def testAddBoundsBatchModeReturnsCorrectNumberOfFiles (self):
        request, response = self.addBoundsCommonSetup()
        request.set_element_BatchMode(True)
        request.set_element_DataColumnNumber(4)
        request, response = self.impl.addBoundsToKineticLaw(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        self.assertEquals(2,len(sbmlfiles))

    def testAddBoundsUsingCorrectDataColumnFromDataFile(self):
        request, response = self.addBoundsCommonSetup()
        request.set_element_DataColumnNumber(5)
        request, response = self.impl.addBoundsToKineticLaw(request, response)
        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)
        self.assertEquals(4.9,sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER_BOUND').getValue())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsSBMLValid']
    unittest.main()
