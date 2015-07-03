'''
Created on 20 Jul 2011

@author: st08574
'''
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




