import unittest

from sbmlmod.facades import ValidateSBMLmodel_facade
from testsbmlmod import resources_folder

class Test_ValidateSBMLmodel_facade(unittest.TestCase):


    def testValidSBMLFileValidatesToTrue(self):
        sbmlfile_lines = open(resources_folder +  'ValidSBML.xml','r').readlines()
        sbmlfile = "".join(sbmlfile_lines)
        [has_errors, listOfErrors] = ValidateSBMLmodel_facade.sbmlFileHasErrors(sbmlfile)
        self.assertFalse(has_errors)

    def testNotValidSBMLFileValidatesToFalse(self):

        sbmlfile_lines = open(resources_folder +  'NonValidSBML.xml','r').readlines()
        sbmlfile = "".join(sbmlfile_lines)

        [has_errors, listOfErrors] = ValidateSBMLmodel_facade.sbmlFileHasErrors(sbmlfile)
        self.assertTrue(has_errors)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
