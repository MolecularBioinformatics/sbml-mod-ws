#!/usr/bin/env python2
# -*- encoding: UTF-8 -*-

# SBMLmod Web Service
# Copyright (C) 2016 Computational Biology Unit, University of Bergen and
#               Molecular Bioinformatics, UiT The Arctic University of Norway
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import base64
import os
import unittest
import zlib

from libsbml import SBMLReader
from libsbml import LIBSBML_VERSION

from sbmlmod.SBMLmod import SBMLmodWS
from sbmlmod.SBMLmod_fault import SBMLmodFault
from sbmlmod.SBMLmod_server import ValidateSBMLModelRequest, \
    ValidateSBMLModelResponse, ReplaceKineticLawParameterRequest, \
    ReplaceKineticLawParameterResponse, ScaleKineticLawParameterRequest, \
    ScaleKineticLawParameterResponse, \
    ReplaceInitialConcentrationsOfSpeciesRequest, \
    ReplaceInitialConcentrationsOfSpeciesResponse, \
    AddKineticLawParameterRequest, AddKineticLawParameterResponse, \
    AddBoundsToKineticLawRequest, AddBoundsToKineticLawResponse
from sbmlmod.facades import version_facade


resources_folder = 'src/testsbmlmod/resources'

class TestSBMLmod(unittest.TestCase):

    def setUp(self):
        self.impl = SBMLmodWS()

    def testValidateModelGzippedBase64EncodedGivesException(self):
        request = ValidateSBMLModelRequest()
        response = ValidateSBMLModelResponse()
        sbmlfile_lines = open(os.path.join(resources_folder, 'ValidSBML.xml'), 'r').readlines()
        sbmlfile = "".join(sbmlfile_lines)
        requestfile = base64.b64encode(sbmlfile)

        request.set_element_SbmlModelFile(requestfile)
        self.assertRaises(SBMLmodFault, self.impl.validateSBMLModelGzippedBase64Encoded, request, response)


    def testFileNotCompressedGivenToValidateSBMLModelGivesException(self):
        request, response = self.validateSBMLModelCommonSetup()
        sbmlfile_lines = open(os.path.join(resources_folder, 'ValidSBML.xml'), 'r').readlines()
        sbmlfile = "".join(sbmlfile_lines)

        request.set_element_SbmlModelFile(sbmlfile)
        self.assertRaises(SBMLmodFault, self.impl.validateSBMLModel, request, response)
        try:
            request, response = self.impl.validateSBMLModel(request, response)
        except SBMLmodFault as e:
            self.assertEquals("FILE_HANDLING_ERROR", e.faultEnum)


    def testWrongFileAsInputToValidateSBMLModelTriggersNotValidModelResponse(self):
        request, response = self.validateSBMLModelCommonSetup()
        sbmlfile_lines = open(os.path.join(resources_folder, 'mapping.txt'), 'r').readlines()
        sbmlfile = "".join(sbmlfile_lines)

        request.set_element_SbmlModelFile(base64.b64encode(zlib.compress(sbmlfile)))
        request, response = self.impl.validateSBMLModel(request, response)

        self.assertFalse(response.get_element_ModelIsValid())
        if LIBSBML_VERSION >= 51300:
            self.assertEquals(1, len(response.get_element_ErrorMessages()))
        else:
            self.assertEquals(2, len(response.get_element_ErrorMessages()))


    def testSBMLFileNotCompressedCorrectlyToReplaceKineticLawParameterRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([filelines])

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testDataFileNotCompressedCorrectlyToReplaceKineticLawParameterRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater.csv'), 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testMappingFileNotCompressedCorrectlyToReplaceKineticLawParameterRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_MappingFile(zlib.compress(filelines))

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testFileEmptyRaisesException(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request.set_element_DataFile("")

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testReplaceKineticLawParameterWorksInBestCase(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request, response = self.impl.replaceKineticLawParameter(request, response)

        modelFile = response.get_element_SbmlModelFiles()[0].SbmlModelFile
        sbmlfile = zlib.decompress(base64.b64decode(modelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmlfile)

        self.assertEquals(472.65, sbmlDocument.getModel().getReaction('R02174').getKineticLaw().getParameter('E_T').getValue())


    def testReplaceKineticLawParameterBatchModeReturnsCorrectNumberOfFiles (self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request.set_element_BatchMode(True)
        request.set_element_DataColumnNumber(3)
        request, response = self.impl.replaceKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()

        self.assertEquals(4, len(sbmlfiles))


    def testReplaceKineticLawParameterReturnsWarnings(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        request, response = self.impl.replaceKineticLawParameter(request, response)
        warnings = response.get_element_Warnings()
        self.assertTrue(warnings)


    def testFileHandlingErrorThrownFromReplaceKineticLawParameterWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater_commaSeparated.csv'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testSBMLFileNotCompressedCorrectlyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([filelines])

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testDataFileNotCompressedCorrectlyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater.csv'), 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testMappingFileNotCompressedCorrectlyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_MappingFile(zlib.compress(filelines))

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testFileEmptyToScaleKineticLawParameterRaisesException(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        request.set_element_DataFile("")

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testFileHandlingErrorThrownFromScaleKineticLawParameterWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater_commaSeparated.csv'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.scaleKineticLawParameter, request, response)


    def testScaleKineticLawParameterWorksInBestCase(self):
        request, response = self.scaleKineticLawParameterCommonSetup()
        request, response = self.impl.scaleKineticLawParameter(request, response)

        modelFile = response.get_element_SbmlModelFiles()[0]
        sbmlfile = zlib.decompress(base64.b64decode(modelFile.SbmlModelFile))

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

        self.assertEquals(4, len(sbmlfiles))


    def testSBMLFileNotCompressedCorrectlyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([filelines])

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testDataFileNotCompressedCorrectlyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'expression_glu_ace_Oh_etal.dat'), 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testMappingFileNotCompressedCorrectlyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping.txt'), 'r'))
        request.set_element_MappingFile(zlib.compress(filelines))

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testFileEmptyToAddKineticLawParameterRaisesException(self):
        request, response = self.addKineticLawParameterCommonSetup()
        request.set_element_SbmlModelFiles([""])

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testFileHandlingErrorThrownFromAddKineticLawParameterWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater_commaSeparated.csv'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testAddKineticLawParameterUsingDefaultOnly(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()

        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DefaultValue(1000)
        request.set_element_ParameterId('UPPER')

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(1000, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        self.assertEquals(1000, sbmlDocument.getModel().getReaction('SYN').getKineticLaw().getParameter('UPPER').getValue())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())


    def testAddKineticLawParameterUsingDataOnlyWithoutMapping(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()

        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open(os.path.join(resources_folder, 'EnzymeIdAsKey.dat'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request.set_element_ParameterId('UPPER')
        request.set_element_DefaultValue(1000)

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        # self.assertTrue(sbmlDocument.getModel().getReaction('SYN').getKineticLaw())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmlfiles[0].SbmlModelFile)
        request, response = self.impl.validateSBMLModel(request, response)
        self.assertTrue(response.get_element_ModelIsValid())


    def testAddKineticLawParameterUsingDataAndDefaultWithoutMapping(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()

        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open(os.path.join(resources_folder, 'EnzymeIdAsKey.dat'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request.set_element_ParameterId('UPPER')
        request.set_element_DefaultValue(1000)

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        self.assertEquals(1000, sbmlDocument.getModel().getReaction('SYN').getKineticLaw().getParameter('UPPER').getValue())

        request, response = self.validateSBMLModelCommonSetup()
        request.set_element_SbmlModelFile(sbmldecomp)
        request, response = self.impl.validateSBMLModelText(request, response)
        self.assertTrue(response.get_element_ModelIsValid())


    def testAddKineticLawParameterUsingDataOnlyWithMapping(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping.txt'), 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'expression_glu_ace_Oh_etal.dat'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DataColumnNumber(3)
        request.set_element_ParameterId('UPPER')
        request.set_element_DefaultValue(1000)

        request, response = self.impl.addKineticLawParameter(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(4.9, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        # self.assertFalse(sbmlDocument.getModel().getReaction('SYN').getKineticLaw())

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

        self.assertEquals(4.9, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER').getValue())
        self.assertEquals(1000, sbmlDocument.getModel().getReaction('SYN').getKineticLaw().getParameter('UPPER').getValue())

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

        self.assertEquals(3, len(sbmlfiles))


    def testAddKineticLawParameterReturnsRaisesFaultWhenWrongMappingFileIsUsed(self):
        request, response = self.addKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.addKineticLawParameter, request, response)


    def testSBMLFileNotCompressedCorrectlyToReplaceInitialConcentrationsOfSpeciesRaisesException(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([filelines])
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.replaceInitialConcentrationsOfSpecies, request, response)


    def testMappingFileNotCompressedCorrectlyToReplaceInitialConcentrationsOfSpeciesRaisesException(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_DataFile(filelines)

        self.assertRaises(SBMLmodFault, self.impl.replaceInitialConcentrationsOfSpecies, request, response)


    def testFileHandlingErrorThrownFromReplaceInitialConcentrationsWhenDataFileIsNotTabDelimitedOrContainsUnEvenNumberOfColumns(self):
        request, response = self.replaceKineticLawParameterCommonSetup()
        filelines = "".join(open(os.path.join(resources_folder, 'InitialConc_acetateCommaSeparated.txt'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))

        self.assertRaises(SBMLmodFault, self.impl.replaceKineticLawParameter, request, response)


    def testReplaceInitialConcentrationsOfSpeciesWorksInBestCase(self):
        request = ReplaceInitialConcentrationsOfSpeciesRequest()
        response = ReplaceInitialConcentrationsOfSpeciesResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open(os.path.join(resources_folder, 'InitialConc_acetate.txt'), 'r'))
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
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        filelines = "".join(open(os.path.join(resources_folder, 'InitialConc_acetate.txt'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        request, response = self.impl.replaceInitialConcentrationsOfSpecies(request, response)
        warnings = response.get_element_Warnings()
        self.assertTrue(warnings)


    def testAddDefaultBoundsToKineticLawParameter(self):
        request = AddBoundsToKineticLawRequest()
        response = AddBoundsToKineticLawResponse()

        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        sbml = base64.b64encode(zlib.compress(filelines))
        request.set_element_SbmlModelFiles([sbml])
        request.set_element_DefaultValue(1000)

        request, response = self.impl.addBoundsToKineticLaw(request, response)

        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)

        self.assertEquals(1000, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER_BOUND').getValue())
        self.assertEquals(0.0, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('LOWER_BOUND').getValue())

        self.assertEquals(1000, sbmlDocument.getModel().getReaction('ACN').getKineticLaw().getParameter('UPPER_BOUND').getValue())
        self.assertEquals(-1000, sbmlDocument.getModel().getReaction('ACN').getKineticLaw().getParameter('LOWER_BOUND').getValue())

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

        self.assertEquals(2, len(sbmlfiles))


    def testAddBoundsUsingCorrectDataColumnFromDataFile(self):
        request, response = self.addBoundsCommonSetup()
        request.set_element_DataColumnNumber(5)
        request, response = self.impl.addBoundsToKineticLaw(request, response)
        sbmlfiles = response.get_element_SbmlModelFiles()
        sbmldecomp = zlib.decompress(base64.b64decode(sbmlfiles[0].SbmlModelFile))

        reader = SBMLReader()
        sbmlDocument = reader.readSBMLFromString(sbmldecomp)
        self.assertEquals(4.9, sbmlDocument.getModel().getReaction('CS').getKineticLaw().getParameter('UPPER_BOUND').getValue())


    # helper functions
    # ================
    def validateSBMLModelCommonSetup(self):
        request = ValidateSBMLModelRequest()
        response = ValidateSBMLModelResponse()
        return request, response


    def replaceKineticLawParameterCommonSetup(self):
        request = ReplaceKineticLawParameterRequest()
        response = ReplaceKineticLawParameterResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater.csv'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        sbml = [base64.b64encode(zlib.compress(filelines))]
        request.set_element_SbmlModelFiles(sbml)
        request.set_element_ParameterId("E_T")
        request.set_element_DataColumnNumber(2)
        return request, response


    def scaleKineticLawParameterCommonSetup(self):
        request = ScaleKineticLawParameterRequest()
        response = ScaleKineticLawParameterResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping_applied_rat.txt'), 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'TestingAvGenuttryksformater.csv'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'TRPcatabolism.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_ParameterId("E_T")
        request.set_element_DataColumnNumber(2)
        request.set_element_MergeMode('MIN')
        return request, response


    def addKineticLawParameterCommonSetup(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping.txt'), 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'expression_glu_ace_Oh_etal.dat'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DataColumnNumber(3)
        request.set_element_DefaultValue(1000)
        request.set_element_MergeMode("MIN")
        request.set_element_ParameterId('UPPER')
        return request, response


    def addBoundsCommonSetup(self):
        request = AddKineticLawParameterRequest()
        response = AddKineticLawParameterResponse()
        filelines = "".join(open(os.path.join(resources_folder, 'mapping.txt'), 'r'))
        request.set_element_MappingFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'expression_glu_ace_Oh_etal.dat'), 'r'))
        request.set_element_DataFile(base64.b64encode(zlib.compress(filelines)))
        filelines = "".join(open(os.path.join(resources_folder, 'SBMLwithoutKinetics.xml'), 'r'))
        request.set_element_SbmlModelFiles([base64.b64encode(zlib.compress(filelines))])
        request.set_element_DataColumnNumber(3)
        request.set_element_DefaultValue(1000)

        return request, response
    # --



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testIsSBMLValid']
    unittest.main()
