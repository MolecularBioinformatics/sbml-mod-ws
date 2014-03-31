'''
Created on 4 Nov 2010

@author: st08574
'''
from sbmledit.SBMLEditFault import SBMLEditFault
class ModelEditor(object):
    '''
    classdocs
    '''


    # Takes a model, a list of reaction Ids with some values, as well as a parameter that should be updated
    # Returns a new model with the new values inserted for a particular parameter
    def replaceKineticLawParameter(self,document,data,column,datainfo,parameter,warnings):
        model = document.getModel()
        newmodel = model.clone()

        reactions = newmodel.getListOfReactions()

        keysNotInData=0
        listKeysNotInData=''

        for reaction in reactions:
            if reaction.getId() in datainfo:
                if not reaction.getKineticLaw():
                    message = "Kinetic law is missing from reaction."
                    raise SBMLEditFault(message, "INTERNAL_ERROR")
                params = reaction.getKineticLaw().getListOfParameters()
                self.found=False
                for e in params:
                    if parameter.lower() in e.getId().lower():
                        e.setValue(data[datainfo.index(reaction.getId())][column])
                        self.found=True
            else:
                keysNotInData+=1
                listKeysNotInData = listKeysNotInData + ' ' + reaction.getId()

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: '+str(keysNotInData)+' of '+str(len(newmodel.getListOfReactions()))+'.')
            warnings.append('The reaction id not found are: '+str(listKeysNotInData))

#        for key in datainfo:
#
#            if newmodel.getReaction(key)!= None :
#
#                reac = newmodel.getReaction(key)
#
#                params = reac.getKineticLaw().getListOfParameters()
#                self.found=False
#                for e in params:
#                    if parameter.lower() in e.getId().lower():
#                        e.setValue(data[datainfo.index(key)][column])
#                        self.found=True
##                if not self.found:
##                    warnings.append("edit: "+parameter + ' not found in reaction ' + key)
#            else:
#                warnings.append(key + ' not found in model')

        return newmodel,warnings

    # Takes a model, a list of reaction IDs with some values, as well as a parameter that should be updated
    # Returns a new model where the old values for a particular parameter have been multiplied with the new values
    def scaleKineticLawParameter(self,document,data,column,datainfo,parameter,warnings):
        model = document.getModel()
        newmodel = model.clone()

        for key in datainfo:

            if newmodel.getReaction(key)!= None :
                oldparams = model.getReaction(key).getKineticLaw().getListOfParameters()
                newparams = newmodel.getReaction(key).getKineticLaw().getListOfParameters()
                self.oldval = None
                self.found=False
                for f in oldparams:
                    if parameter.lower() in f.getId().lower():
                        self.oldval = f.getValue()
                        self.found=True
                if self.found:
                    for e in newparams:
                        if parameter.lower() in e.getId().lower():
                            e.setValue(self.oldval*data[datainfo.index(key)][column])

                else:
                    warnings.append("scale: "+parameter + ' not found in reaction ' + key)

            else: warnings.append(key + ' not found in model')

        return newmodel, warnings


    # Takes a model and a list of metabolites and initial concentrations
    # Returns a new model with the new initial concentrations
    def editInitialConcentrations(self, document, data, datainfo, warnings,column):

        model = document.getModel()
        newmodel = model.clone()

        keysNotInModel=0
        listKeysNotInModel=''

        for key in datainfo:
            if newmodel.getSpecies(key)!=None:
                newmodel.getSpecies(key).setInitialConcentration(data[datainfo.index(key)][column])
            else:
                keysNotInModel+=1
                listKeysNotInModel=listKeysNotInModel+ ' '+key

        warnings.append(str(keysNotInModel) + 'species from the model are not found in the data file. The default value have been entered for these species.')
        warnings.append('The keys  not found are: '+str(listKeysNotInModel))

        return newmodel,warnings

    def addKineticLawParameter(self,document,parameter,warnings,default_value=None,data=None,datainfo=None,column=0):

        model = document.getModel()
        newmodel = model.clone()

        keysNotInData=0
        listKeysNotInData=''

        reactions = newmodel.getListOfReactions()
        for reaction in reactions:
            if not reaction.isSetKineticLaw():
                reaction.createKineticLaw()
            reaction.getKineticLaw().createParameter().setId(parameter)
            if data and reaction.getId() in datainfo:
                reaction.getKineticLaw().getParameter(parameter).setValue(data[datainfo.index(reaction.getId())][column])
            else:
                reaction.getKineticLaw().getParameter(parameter).setValue(default_value)

            if data and reaction.getId() not in datainfo:
                keysNotInData = keysNotInData+1
                listKeysNotInData=listKeysNotInData+ ' '+reaction.getId()

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: '+str(keysNotInData)+' of '+str(len(newmodel.getListOfReactions()))+'. Default value: '+str(default_value)+' has been inserted to these reactions.')
            warnings.append('The reaction id  not found are: '+str(listKeysNotInData))

        return newmodel,warnings

    def addBounds(self,document,warnings,default_value=1000,data=None,datainfo=None,column=0):
        model = document.getModel()
        newmodel = model.clone()
        upper='UPPER_BOUND'
        lower='LOWER_BOUND'

        keysNotInData=0
        listKeysNotInData=''

        reactions = newmodel.getListOfReactions()
        for reaction in reactions:
            if not reaction.isSetKineticLaw():
                reaction.createKineticLaw()
            reaction.getKineticLaw().createParameter().setId(upper)
            reaction.getKineticLaw().createParameter().setId(lower)

            if data and reaction.getId() in datainfo:
                reaction.getKineticLaw().getParameter(upper).setValue(data[datainfo.index(reaction.getId())][column])
                if reaction.getReversible():
                    reaction.getKineticLaw().getParameter(lower).setValue(-data[datainfo.index(reaction.getId())][column])
                else:
                    reaction.getKineticLaw().getParameter(lower).setValue(0.0)
            else:
                reaction.getKineticLaw().getParameter(upper).setValue(default_value)

                if reaction.getReversible():
                    reaction.getKineticLaw().getParameter(lower).setValue(-default_value)
                else:
                    reaction.getKineticLaw().getParameter(lower).setValue(0.0)

            if data and reaction.getId() not in datainfo:
                keysNotInData = keysNotInData+1
                listKeysNotInData=listKeysNotInData+ ' '+reaction.getId()

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: '+str(keysNotInData)+' of '+str(len(newmodel.getListOfReactions()))+'. Default value: '+str(default_value)+' has been inserted to these reactions.')
            warnings.append('The reaction id  not found are: '+str(listKeysNotInData))

        return newmodel,warnings

    def replaceGlobalParameters(self, document, data,column,datainfo, warnings, header=True ):
        model = document.getModel()
        newmodel = model.clone()

        for key in datainfo:
            if newmodel.getParameter(key)!=None:
                param = newmodel.getParameter(key)
                param.setValue(data[datainfo.index(key)][column])
            else:
                warnings.append(key + ' (GlobalParameter) not found in model')

        return newmodel,warnings


    def scaleGlobalParameters(self, document, data,column,datainfo, warnings, header=True ):
        model = document.getModel()
        newmodel = model.clone()

        for key in datainfo:

            if newmodel.getParameter(key)!=None:
                param = newmodel.getParameter(key)
                oldval = param.getValue()
                param.setValue(oldval*data[datainfo.index(key)][column])
            else:
                warnings.append(key + ' (GlobalParameter) not found in model')

        return newmodel,warnings


