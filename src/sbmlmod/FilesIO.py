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
import zlib

from libsbml import SBMLReader, SBMLWriter
from sbmlmod.SBMLmod_fault import SBMLmodFault
from sbmlmod.SBMLmod_types import ns0 as SBMLfiletypeNs


class FilesIO:

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


    def getMappingFile(self, request):
        try:
            mappingfile = zlib.decompress(base64.b64decode(request.get_element_MappingFile())).strip()
        except:
            message = "The mapping file could not be decompressed, ensure file is not empty, zipped and then encoded as a string."
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
