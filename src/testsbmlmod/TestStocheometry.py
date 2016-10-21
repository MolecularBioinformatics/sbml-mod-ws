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

from libsbml import SBMLReader

from sbmlmod import Stocheometry


class TestModelEditor(unittest.TestCase):

    def setUp(self):
        filepath = "./resources/ValidSBML.xml"

        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        self.sbml = self.doc.getModel()
        self.stoch = Stocheometry.Stocheometry()



    def testCalculateStocheometryMatrix(self):

        self.stoch.calculateStocheometryMatrix(self.doc)

        matrix = self.stoch.getStocheometryMatrix()

        self.assertEquals(matrix[6][3], 1)
        self.assertEquals(matrix[6][4], -1)

    def testSetSpeciesExtOrInt(self):
        self.stoch.calculateStocheometryMatrix(self.doc)
        model = self.stoch.setSpeciesExtOrInt(self.doc, self.stoch.getStocheometryMatrix())

        self.assertTrue(model.getListOfSpecies()[0].getBoundaryCondition() == True)
        self.assertFalse(model.getListOfSpecies()[5].getBoundaryCondition() == True)




if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()




