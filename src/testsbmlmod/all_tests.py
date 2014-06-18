import unittest

from testsbmlmod.facades.version_facade import Test_version_facade
from testsbmlmod.facades.ValidateSBMLmodel_facade import Test_ValidateSBMLmodel_facade
from testsbmlmod.TestSBMLmod import TestSBMLmod

def main():
    suite = unittest.TestSuite()
    #add the different test classes
    suite.addTest(unittest.makeSuite(TestSBMLmod))

    suite.addTest(unittest.makeSuite(Test_version_facade))
    suite.addTest(unittest.makeSuite(Test_ValidateSBMLmodel_facade))



    #run the test suite
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
