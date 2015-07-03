import unittest

from sbmlmod import DataMapper
from sbmlmod.SBMLmod_fault import SBMLmodFault


class TestDataMapper(unittest.TestCase):

    def testMapExpressionToEnzymesDefault(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'GenSymbol\tExpr_verdi\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Gen_navn\tExpr1\tExpr2\tExpr3\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper.setup(mapinput, exprinput, 3)

        ret = mapper.mergeExpressionValuesMappingToSameReaction()

        testexpr = ret[0]
        testinfo = ret[1]

        self.assertEquals(78.2, testexpr[testinfo.index('TPH')][0])

    def testMapExpressionToEnzymes_SumMode(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper.setup(mapinput, exprinput, 3)

        ret = mapper.mergeExpressionValuesMappingToSameReaction(mode='SUM')

        testexpr = ret[0]
        testinfo = ret[1]

        self.assertEquals(87.8, testexpr[testinfo.index('TPH')][0])

    def testMapExpressionToEnzymes_MedianMode(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2\nTPH\tTph3'
        exprinput = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9\nTph3\t67.4\t23.6\t6.8'

        mapper.setup(mapinput, exprinput, 3)

        ret = mapper.mergeExpressionValuesMappingToSameReaction(mode='MEDIAN')

        testexpr = ret[0]
        testinfo = ret[1]

        self.assertEquals(23.6, testexpr[testinfo.index('TPH')][0])


    def testSetupMappingType(self):
        mapper = DataMapper.DataMapper()
        input = 'IDO\tIndo1\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nTPH\tTph2'

        testobj = mapper.setup_mapping(input)

        self.assertTrue(type({}) == type(testobj))

    def testSetupMappingContent(self):
        mapper = DataMapper.DataMapper()
        input = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'

        response = mapper.setup_mapping(input)

        genes = response['TPH']

        self.assertEquals('Tph1', genes[0])
        self.assertEquals('Tph2', genes[1])

    def testSetupMappingFileContainingOneColumnRaisesException(self):
        mapper = DataMapper.DataMapper()
        input = 'IDO\nTDO\nTPH\nIDOnTPH'

        self.assertRaises(SBMLmodFault, mapper.setup_mapping, input)


    def testSetupExprType(self):

        mapping_string = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        mapper = DataMapper.DataMapper()
        mapping = mapper.setup_mapping(mapping_string)


        input = 'Indo1\t24.3\t78.2\t97.0\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nTph2\t0.23\t9.6\t4.9'

        testexpr, testinfo = mapper.setup_expr(input, 2)

        self.assertTrue(type([[]]) == type(testexpr))
        self.assertTrue(type([]) == type(testinfo))


    def testSetupExprContent(self):
        mapping_string = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        mapper = DataMapper.DataMapper()
        mapping = mapper.setup_mapping(mapping_string)
        input = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        testexpr, testinf = mapper.setup_expr(input, 3, header=False)
        index = testinf.index('Indo2')

        self.assertAlmostEquals(982.8, testexpr[index][0])


    def testSetupExprIndexOutOfBoundsExceptionHandling(self):
        mapper = DataMapper.DataMapper()
        input = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        self.assertRaises(SBMLmodFault, mapper.setup_expr, input, 5)


    def testSetupExprDataColumnNotContainingFloatRaisesException(self):
        mapper = DataMapper.DataMapper()
        input = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'

        self.assertRaises(SBMLmodFault, mapper.setup_expr, input, 1)


    def testMergeExpression_addMode(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2']}
        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        testexpr, testinfo = mapper.sumExpression(mapping, expr, info)

        self.assertEquals(52.2, testexpr[testinfo.index('IDO',)][0])
        self.assertAlmostEquals(134.9, testexpr[testinfo.index('TPH')][0])

    def testMergeExpression_MaxMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2']}
        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        testexpr, testinfo = mapper.maxExpression(mapping, expr, info)

        self.assertEquals(26.3, testexpr[testinfo.index('IDO',)][0])
        self.assertEquals(89.6, testexpr[testinfo.index('TPH')][0])

    def testMergeExpression_MinMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2']}
        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        testexpr, testinfo = mapper.minExpression(mapping, expr, info)

        self.assertEquals(25.9, testexpr[testinfo.index('IDO',)][0])
        self.assertEquals(45.3, testexpr[testinfo.index('TPH')][0])

    def testMergeExpression_MeanMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2']}
        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        testexpr, testinfo = mapper.meanExpression(mapping, expr, info)

        self.assertEquals(26.1, testexpr[testinfo.index('IDO',)][0])
        self.assertAlmostEqual(67.45, testexpr[testinfo.index('TPH')][0])

    def testMergeExpression_MedianMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2', 'Tph3']}
        expr = [[95.3], [25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Tph3', 'Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        testexpr, testinfo = mapper.medianExpression(mapping, expr, info)

        self.assertEquals(26.1, testexpr[testinfo.index('IDO',)][0])
        self.assertEquals(89.6, testexpr[testinfo.index('TPH',)][0])


    def testCheckMappingReturnsNoWarning(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2']}
        expr = {'Indo1':25.9, 'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        warning = mapper.checkMapping(mapping, expr)

        self.assertFalse(warning)


    def testCheckMappingReturnsOneWarning(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['Tdo'], 'TPH':['Tph1', 'Tph2']}
        # expr = [[25.9],[26.3],[65],[89.6],[45.3]]
        info = ['Indo1', 'Indo', 'Tdo', 'Tph1', 'Tph2']

        miss = 'Indo2'

        warning = mapper.checkMapping(mapping, info)

        self.assertTrue(miss in "".join(warning))

    def testCheckMappingReturnsWarningsExpressionValueNotFound(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1', 'Indo2'], 'TDO':['TDO'], 'TPH':['Tph1', 'TPH2']}
        info = ['Indo1', 'Indo', 'Tdo', 'Tph1', 'Tph2']

        warning = mapper.checkMapping(mapping, info)

        stringInWarning = False
        for w in warning:
            if "Expression value not found" in w:
                stringInWarning = True
        self.assertTrue(stringInWarning)


    def testEfluxRaisesFaultIfMappingFileContainsTwoColumns(self):
        mapper = DataMapper.DataMapper()
        mapping_string = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo', 'Tdo', 'Tph1', 'Tph2']

        mapping = mapper.setup_mapping(mapping_string)


        self.assertRaises(SBMLmodFault, mapper.eFlux, mapping, expr, info)

    def testEfluxRaisesFaultIfGenesMissAnnotationInThirdColumnOfMappingFile(self):
        mapper = DataMapper.DataMapper()
        mapping_string = 'IDO\tIndo2\tISO\nTDO\tTdo\t\nTPH\tTph1\t\nIDO\tIndo1\tISO\nTPH\tTph2\t'

        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo', 'Tdo', 'Tph1', 'Tph2']

        mapping = mapper.setup_mapping(mapping_string)


        self.assertRaises(SBMLmodFault, mapper.eFlux, mapping, expr, info)

    def testEfluxMergesISOcorrectly(self):
        mapper = DataMapper.DataMapper()
        mapping_string = 'IDO\tIndo2\tISO\nTDO\tTdo\t\nTPH\tTph1\tCOMPLEX\nIDO\tIndo1\tISO\nTPH\tTph2\tCOMPLEX'

        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        mapping = mapper.setup_mapping(mapping_string)

        mexpr, minfo = mapper.eFlux(mapping, expr, info)

        self.assertTrue(52.2, mexpr[minfo.index('IDO')][0])

    def testEfluxMergesCOMPLEXcorrectly(self):
        mapper = DataMapper.DataMapper()
        mapping_string = 'IDO\tIndo2\tISO\nTDO\tTdo\t\nTPH\tTph1\tCOMPLEX\nIDO\tIndo1\tISO\nTPH\tTph2\tCOMPLEX'

        expr = [[25.9], [26.3], [65], [89.6], [45.3]]
        info = ['Indo1', 'Indo2', 'Tdo', 'Tph1', 'Tph2']

        mapping = mapper.setup_mapping(mapping_string)

        mexpr, minfo = mapper.eFlux(mapping, expr, info)
        self.assertTrue(45.3, mexpr[minfo.index('TPH')][0])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
