import unittest

from sbmlmod.facades import version_facade


class Test_version_facade(unittest.TestCase):


    def setUp(self):
        pass

    def testGetVersion(self):
        self.assertEquals (version_facade.getVersion(), '0.1.6')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testIsSBMLValid']
    unittest.main()
