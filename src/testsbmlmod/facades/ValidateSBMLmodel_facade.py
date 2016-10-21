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

import unittest

from sbmlmod.facades import ValidateSBMLmodel_facade
from testsbmlmod import resources_folder


class Test_ValidateSBMLmodel_facade(unittest.TestCase):


    def testValidSBMLFileValidatesToTrue(self):
        sbmlfile_lines = open(resources_folder + 'ValidSBML.xml', 'r').readlines()
        sbmlfile = "".join(sbmlfile_lines)
        [has_errors, listOfErrors] = ValidateSBMLmodel_facade.sbmlFileHasErrors(sbmlfile)
        self.assertFalse(has_errors)

    def testNotValidSBMLFileValidatesToFalse(self):

        sbmlfile_lines = open(resources_folder + 'NonValidSBML.xml', 'r').readlines()
        sbmlfile = "".join(sbmlfile_lines)

        [has_errors, listOfErrors] = ValidateSBMLmodel_facade.sbmlFileHasErrors(sbmlfile)
        self.assertTrue(has_errors)



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
