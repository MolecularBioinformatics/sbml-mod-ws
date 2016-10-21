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

from testsbmlmod.TestSBMLmod import TestSBMLmod
from testsbmlmod.facades.ValidateSBMLmodel_facade import Test_ValidateSBMLmodel_facade
from testsbmlmod.facades.version_facade import Test_version_facade


def main():
    suite = unittest.TestSuite()
    # add the different test classes
    suite.addTest(unittest.makeSuite(TestSBMLmod))

    suite.addTest(unittest.makeSuite(Test_version_facade))
    suite.addTest(unittest.makeSuite(Test_ValidateSBMLmodel_facade))



    # run the test suite
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
