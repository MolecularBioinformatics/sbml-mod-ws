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

from libsbml import SBMLReader, SBMLWriter


def sbmlFileHasErrors(sbml_file):
    reader = SBMLReader()
    document = reader.readSBMLFromString(sbml_file)
    number_of_errors = document.getNumErrors()
    has_errors = number_of_errors > 0
    listOfErrors = []
    if number_of_errors:
        for error in range(number_of_errors):
            listOfErrors.append(document.getErrorLog().getError(error).getMessage())

    return [has_errors, listOfErrors]
