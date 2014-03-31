'''
Created on 4 Nov 2010

@author: st08574
'''
import unittest
from sbmledit import DataMapper
from sbmledit.SBMLEditFault import SBMLEditFault

class TestDataMapper(unittest.TestCase):

    def testMapExpressionToEnzymesDefault(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'GenSymbol\tExpr_verdi\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Gen_navn\tExpr1\tExpr2\tExpr3\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper.setup(mapinput, exprinput, 3)

        testobj, warning = mapper.mergeExpressionValuesMappingToSameReaction()


        self.assertEquals(78.2,testobj['TPH'])

    def testMapExpressionToEnzymes_SumMode(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper.setup(mapinput, exprinput, 3)

        ret = mapper.mergeExpressionValuesMappingToSameReaction(mode='SUM')
        testobj = ret[0]

        self.assertEquals(87.8,testobj['TPH'])


    def testSetupMappingType(self):
        mapper = DataMapper.DataMapper()
        input = 'IDO\tIndo1\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nTPH\tTph2'

        testobj = mapper.setup_mapping(input)

        self.assertTrue(type({})==type(testobj))

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

        self.assertRaises(SBMLEditFault, mapper.setup_mapping,input)


    def testSetupExprType(self):
        mapper = DataMapper.DataMapper()
        input = 'Indo1\t24.3\t78.2\t97.0\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nTph2\t0.23\t9.6\t4.9'

        testobj = mapper.setup_expr(input,2)

        self.assertTrue(type({})==type(testobj))


    def testSetupExprContent(self):
        mapper = DataMapper.DataMapper()
        input = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        testobj = mapper.setup_expr(input,3,header=False)
        self.assertAlmostEquals(982.8, testobj['Indo2'])

    def testSetupExprIndexOutOfBoundsExceptionHandling(self):
        mapper = DataMapper.DataMapper()
        input = 'Indo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        self.assertRaises(SBMLEditFault, mapper.setup_expr,input, 5)


    def testSetupExprDataColumnNotContainingFloatRaisesException(self):
        mapper = DataMapper.DataMapper()
        input = 'IDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'

        self.assertRaises(SBMLEditFault, mapper.setup_expr,input, 1)


    def testMergeExpression_addMode(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2']}
        expr = {'Indo1':25.9,'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        testobj = mapper.sumExpression(mapping,expr)

        self.assertEquals(52.2, testobj['IDO'])
        self.assertAlmostEquals(134.9, testobj['TPH'])

    def testMergeExpression_MaxMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2']}
        expr = {'Indo1':25.9,'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        testobj = mapper.maxExpression(mapping,expr)

        self.assertEquals(26.3, testobj['IDO'])
        self.assertEquals(89.6, testobj['TPH'])

    def testMergeExpression_MinMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2']}
        expr = {'Indo1':25.9,'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        testobj = mapper.minExpression(mapping,expr)

        self.assertEquals(25.9, testobj['IDO'])
        self.assertEquals(45.3, testobj['TPH'])

    def testMergeExpression_MeanMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2']}
        expr = {'Indo1':25.9,'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        testobj = mapper.meanExpression(mapping,expr)

        self.assertEquals(26.1, testobj['IDO'])
        self.assertAlmostEqual(67.45, testobj['TPH'])

    def testMergeExpression_MedianMode(self):

        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2','Tph3']}
        expr = {'Indo1':25.9,'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3, 'Tph3':95.3}

        testobj = mapper.medianExpression(mapping,expr)

        self.assertEquals(26.1, testobj['IDO'])
        self.assertEquals(89.6, testobj['TPH'])


    def testCheckMappingReturnsNoWarning(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2']}
        expr = {'Indo1':25.9,'Indo2':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        warning = mapper.checkMapping(mapping, expr)

        self.assertFalse(warning)


    def testCheckMappingReturnsOneWarning(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['Tdo'],'TPH':['Tph1','Tph2']}
        expr = {'Indo1':25.9,'Indo':26.3, 'Tdo':65, 'Tph1':89.6, 'Tph2':45.3}

        miss = 'Indo2'

        warning = mapper.checkMapping(mapping, expr)

        self.assertTrue(miss in warning[0])

    def testCheckMappingReturnsCorrectAmountOfWarnings(self):
        mapper = DataMapper.DataMapper()
        mapping = {'IDO':['Indo1','Indo2'],'TDO':['TDO'],'TPH':['Tph1','TPH2']}
        expr = {'Indo1':25.9,'Indo':26.3, 'Tdo':65, 'Tph1':89.6}

        warning = mapper.checkMapping(mapping, expr)

        self.assertEquals(3, len(warning))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()