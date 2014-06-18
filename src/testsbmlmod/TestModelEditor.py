import unittest
from libsbml import SBMLReader
from sbmlmod import ModelEditor, DataMapper

class TestModelEditor(unittest.TestCase):


    def setUp(self):
        filepath = "./resources/TRPcatabolism.xml"

        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        self.sbml = self.doc.getModel()
        self.editor = ModelEditor.ModelEditor()

        datastr = ''.join(open('./resources/TestingAvGenuttryksformater.csv','r').readlines()).strip()
        mapstr = ''.join(open('./resources/mapping_applied_rat.txt','r').readlines()).strip()

        mapper = DataMapper.DataMapper()
        mapper.setup(mapstr, datastr, batch=True)
        return mapper.mergeExpressionValuesMappingToSameReaction()

    def setUp2(self):

        filepath = "./resources/SimplifiedModel2.xml"
        datastr = ''.join(open('./resources/RNAseq_M58_a522.txt','r').readlines()).strip()
        mapstr = ''.join(open('./resources/mappingNeisseria.txt','r').readlines()).strip()

        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)
        self.sbml = self.doc.getModel()
        self.editor = ModelEditor.ModelEditor()

        mapper = DataMapper.DataMapper()
        mapper.setup(mapstr, datastr, col=11,batch=True)
        return mapper.mergeExpressionValuesMappingToSameReaction()

    def setUpGlobal(self):
        filepath = "./resources/TRP_mammal_turnover_Oxy_GlobalParameters.xml"

        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        self.sbml = self.doc.getModel()
        self.editor = ModelEditor.ModelEditor()

        datastr = ''.join(open('./resources/TestingAvGenuttryksformater.csv','r').readlines()).strip()
        mapstr = ''.join(open('./resources/mappingRat_GlobalParameters.txt','r').readlines()).strip()

        mapper = DataMapper.DataMapper()
        mapper.setup(mapstr, datastr)
        return mapper.mergeExpressionValuesMappingToSameReaction()



    def testReplaceKineticLawParameter(self):

        ret = self.setUp()
        expression = ret[0]
        info = ret[1]
        warning = ret[2]
        column=0
        parameter='E_T'

        newsbml,warning = self.editor.replaceKineticLawParameter(self.doc,expression,column,info,parameter,warning)

        testobj = newsbml.getReaction('R00678_TDO').getKineticLaw().getParameter('E_T').getValue()

        self.assertEquals(expression[info.index('R00678_TDO')][column],testobj)


    def testReplaceKineticLawParameterReturnsWarning(self):

        ret = self.setUp()
        expression = ret[0]
        info = ret[1]
        warning = ret[2]
        column=0
        parameter='E_T'

        newsbml,warning = self.editor.replaceKineticLawParameter(self.doc,expression,column,info,parameter,warning)


        self.assertTrue('R03664' in ''.join(warning))

    def testReplaceGlobalParameter(self):

        ret = self.setUpGlobal()
        expression = ret[0]
        info = ret[1]
        warning = ret[2]
        column=0

        newsbml,warning = self.editor.replaceGlobalParameters(document=self.doc,data=expression,column=column,datainfo=info,warnings=warning)

        testobj = newsbml.getParameter('DDC_E_T').getValue()

        self.assertEquals(expression[info.index('DDC_E_T')][column],testobj)


    def testReplaceGlobalParameterReturnsWarning(self):

        ret = self.setUpGlobal()
        expression = ret[0]
        info = ret[1]
        warning = ret[2]
        column=0

        info.append('GlobalMickeyMouse')
        expression.append(expression[0])

        newsbml,warning = self.editor.replaceGlobalParameters(document=self.doc,data=expression,column=column,datainfo=info,warnings=warning)

        self.assertTrue('GlobalMickeyMouse' in ''.join(warning))

    def testScaleKineticLawParameter(self):

        ret = self.setUp()
        expression = ret[0]
        info = ret[1]
        column=0
        parameter='E_T'

        newsbml,warning = self.editor.scaleKineticLawParameter(document=self.doc,data=expression,column=0,datainfo=info,parameter=parameter,warnings=[])

        testobj = newsbml.getReaction('R00678_TDO').getKineticLaw().getParameter('E_T').getValue()
        oldvalue = self.doc.getModel().getReaction('R00678_TDO').getKineticLaw().getParameter('E_T').getValue()
        scalingvalue = expression[info.index('R00678_TDO')][column]

        self.assertEquals(oldvalue*scalingvalue,testobj)

    def testScaleKineticLawParameterReturnsWarning(self):

        ret = self.setUp()
        expression = ret[0]
        info = ret[1]

        parameter='E_T'

        info.append('ScaleMickeyMouse')
        expression.append(expression[0])

        newsbml,warning = self.editor.scaleKineticLawParameter(document=self.doc,data=expression,column=0,datainfo=info,parameter=parameter,warnings=[])

        self.assertTrue('ScaleMickeyMouse' in ''.join(warning))

    def testEditInitialConcentrations(self):

        data=[[0.4],[0.00030],[0.70]]

        info=['M_3hanthrn_c','M_Lfmkynr_c','tull']

        newsbml, warning = self.editor.editInitialConcentrations(document=self.doc,data=data,datainfo=info,warnings=[],column=0)

        testobj = newsbml.getSpecies('M_Lfmkynr_c').getInitialConcentration()
        self.assertEquals(data[1][0],testobj)

    def testEditInitialConcentrationsReturnsCorrectWarning(self):

        data=[[0.4],[0.00030],[0.70]]

        info=['M_3hanthrn_c','M_Lfmkynr_c','tull']

        newsbml, warning = self.editor.editInitialConcentrations(document=self.doc,data=data,datainfo=info,warnings=[],column=0)
        warning = ''.join(warning)

        self.assertTrue('tull' in warning)


    def testAddDefaultParameterToKineticLawParameter(self):

        self.setUp()


        newsbml, warning = self.editor.addKineticLawParameter(self.doc,'MyNewParameter',[],9.0)


        for r in newsbml.getListOfReactions():
            testobj = r.getKineticLaw().getParameter('MyNewParameter').getValue()
            self.assertEquals(9.0,testobj)

    def testAddKineticLawParameter(self):

        expr = self.setUp2()

        #newsbml,warning = self.editor



    def testAddNewParameterAndDataWithoutMappingToKineticLawParameter(self):
        filepath = "./resources/SBMLwithoutKinetics.xml"
        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        self.doc.getModel()

        datastr = 'GeneName\tDataValue1\tDataValue2\tDataValue3\nCS\t46.8\t982.8\t9.6\nACN\t83.5\t45.9\t73.9\nICD\t37.2\t78.2\t23.0\nKDH\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper = DataMapper.DataMapper()
        datavals,datainfo = mapper.setup_expr(datastr,3)

        newsbml, warning = self.editor.addKineticLawParameter(self.doc,'UPPER_BOUND',[],data=datavals,datainfo=datainfo,default_value=1000)

        testobj = newsbml.getReaction('ICD').getKineticLaw().getParameter('UPPER_BOUND').getValue()

        self.assertEquals(testobj,78.2)

    def testAddDefaultParameterIfReactionNotInDataFile(self):
        filepath = "./resources/SBMLwithoutKinetics.xml"
        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        self.doc.getModel()

        datastr = 'GeneName\tDataValue1\tDataValue2\tDataValue3\nCS\t46.8\t982.8\t9.6\nACN\t83.5\t45.9\t73.9\nICD\t37.2\t78.2\t23.0\nKDH\t24.3\t78.2\t97.0\nTph2\t0.23\t9.6\t4.9'

        mapper = DataMapper.DataMapper()
        datavals,datainfo = mapper.setup_expr(datastr,batch=True)

        newsbml, warning = self.editor.addKineticLawParameter(self.doc,'UPPER_BOUND',[],9.0,data=datavals,datainfo=datainfo)

        right_value=False
        for r in newsbml.getListOfReactions():
            testobj = r.getKineticLaw().getParameter('UPPER_BOUND').getValue()
            right_value=False
            if testobj==9.0 or testobj==datavals[datainfo.index(r.getId())][0]:
                right_value=True
            self.assertTrue(right_value)


    def testWarningAddedWhenReactionIdNotFoundInData(self):
        filepath = "./resources/SBMLwithoutKinetics.xml"
        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        self.doc.getModel()

        values = [[0.999],[0.883],[0.777]]
        info = ['CS','ACN','ICD']

        newsbml, warning = self.editor.addKineticLawParameter(self.doc,'UPPER_BOUND',[],1000,data=values,datainfo=info,column=0)



        warning = ''.join(warning)
        self.assertTrue('ScAS' in warning)



    def testIrreversibleReactionGetsZeroLowerBoundInAddBoundsToKineticLawParameter(self):
        filepath = "./resources/SBMLwithoutKinetics.xml"
        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        values = [[0.999],[0.883],[0.777]]
        info = ['CS','ACN','tull']

        newsbml,warning = self.editor.addBounds(self.doc,[],10, values, info)

        self.assertEquals(newsbml.getReaction('CS').getKineticLaw().getParameter('LOWER_BOUND').getValue(),0.0)

    def testReversibleReactionGetsUpperAndLowerBoundInAddBoundsToKineticLawParameter(self):
        filepath = "./resources/SBMLwithoutKinetics.xml"
        reader = SBMLReader()
        self.doc = reader.readSBMLFromFile(filepath)

        values = [[0.999],[0.883],[0.777]]
        info = ['CS','ACN','tull']

        newsbml,warning = self.editor.addBounds(self.doc, [],10,values,info)

        upper = newsbml.getReaction('ACN').getKineticLaw().getParameter('UPPER_BOUND').getValue()
        lower = newsbml.getReaction('ACN').getKineticLaw().getParameter('LOWER_BOUND').getValue()

        self.assertEquals(upper,lower*-1)








if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
