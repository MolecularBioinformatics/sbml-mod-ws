import unittest

from sbmlmod import DataMapper
from sbmlmod.SBMLmod_fault import SBMLmodFault


class TestDataMapperBatchProcessing(unittest.TestCase):


    def testMapExpressionToEnzymesDefault(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'GenSymbol\tExpr_verdi\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Gen_navn\tExpr1\tExpr2\tExpr3\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t2.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t45.9'

        mapper.setup(mapinput, exprinput, batch=True)

        ret = mapper.mergeExpressionValuesMappingToSameReaction()

        testexpr = ret[0]
        testinfo = ret[1]

        self.assertEquals(78.2, testexpr[testinfo.index('TPH')][1])
        self.assertEquals(37.2, testexpr[testinfo.index('TPH')][0])
        self.assertEquals(73.9, testexpr[testinfo.index('TDO')][2])


    def testCorrectNumberOfColumnsIncludedInDataTable(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'GenSymbol\tExpr_verdi\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Gen_navn\tExpr1\tExpr2\tExpr3\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t23.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper.setup(mapinput, exprinput, batch=True)

        ret = mapper.mergeExpressionValuesMappingToSameReaction()

        testexpr = ret[0]

        self.assertEquals(3, len(testexpr[0]))

    def testMapExpressionToEnzymesSUM(self):
        mapper = DataMapper.DataMapper()
        mapinput = 'GenSymbol\tExpr_verdi\nIDO\tIndo2\nTDO\tTdo\nTPH\tTph1\nIDO\tIndo1\nTPH\tTph2'
        exprinput = 'Gen_navn\tExpr1\tExpr2\tExpr3\nIndo2\t46.8\t982.8\t9.6\nTdo\t83.5\t45.9\t73.9\nTph1\t37.2\t78.2\t2.0\nIndo1\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t45.9'

        mapper.setup(mapinput, exprinput, batch=True)

        ret = mapper.mergeExpressionValuesMappingToSameReaction('SUM')

        testexpr = ret[0]
        testinfo = ret[1]

        self.assertEquals(37.43, testexpr[testinfo.index('TPH')][0])
        self.assertEquals(87.8, testexpr[testinfo.index('TPH')][1])
        self.assertEquals(47.9, testexpr[testinfo.index('TPH')][2])








