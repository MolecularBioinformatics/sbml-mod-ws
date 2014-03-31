'''
Created on 21 Jan 2014

@author: annes
'''

import unittest

from testsbmledit.facades.version_facade import Test_version_facade
from testsbmledit.facades.ValidateSBMLmodel_facade import Test_ValidateSBMLmodel_facade
from testsbmledit.TestSBMLEditImpl import TestSBMLEditImpl

def main():
    suite = unittest.TestSuite()
    #add the different test classes
    suite.addTest(unittest.makeSuite(TestSBMLEditImpl))

    suite.addTest(unittest.makeSuite(Test_version_facade))
    suite.addTest(unittest.makeSuite(Test_ValidateSBMLmodel_facade))



    #run the test suite
    unittest.TextTestRunner(verbosity=2).run(suite)

