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

from sbmlmod.SBMLmod_fault import SBMLmodFault


class ModelEditor(object):

    # Takes a model, a list of reaction Ids with some values, as well as a parameter that should be updated
    # Returns a new model with the new values inserted for a particular parameter
    def replaceKineticLawParameter(self, document, data, column, datainfo, parameter, warnings):
        model = document.getModel()
        newmodel = model.clone()

        reactions = newmodel.getListOfReactions()

        keysNotInData = 0
        listKeysNotInData = []

        for reaction in reactions:
            if reaction.getId() in datainfo:
                if not reaction.getKineticLaw():
                    message = "Kinetic law is missing from reaction."
                    raise SBMLmodFault(message, "INTERNAL_ERROR")

                params = reaction.getKineticLaw().getListOfParameters()
                for e in params:
                    if parameter.lower() in e.getId().lower():
                        e.setValue(data[datainfo.index(reaction.getId())][column])
            else:
                if not reaction.getKineticLaw():
                    message = "Kinetic law is missing from reaction."
                    raise SBMLmodFault(message, "INTERNAL_ERROR")

                params = reaction.getKineticLaw().getListOfParameters()
                found = False
                for e in params:
                    if parameter.lower() in e.getId().lower():
                        found = True
                        break

                if found:
                    keysNotInData += 1
                    listKeysNotInData.append(reaction.getId())

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: {} of {}.'.format(keysNotInData, len(newmodel.getListOfReactions())))
            warnings.append('The reaction IDs not found are: {}'.format(' '.join(listKeysNotInData)))

        return newmodel, warnings


    # Takes a model, a list of reaction IDs with some values, as well as a parameter that should be updated
    # Returns a new model where the old values for a particular parameter have been multiplied with the new values
    def scaleKineticLawParameter(self, document, data, column, datainfo, parameter, warnings):
        model = document.getModel()
        newmodel = model.clone()

        reactions = newmodel.getListOfReactions()

        keysNotInData = 0
        listKeysNotInData = []

        for reaction in reactions:
            if reaction.getId() in datainfo:
                if not reaction.getKineticLaw():
                    message = "Kinetic law is missing from reaction."
                    raise SBMLmodFault(message, "INTERNAL_ERROR")

                params = reaction.getKineticLaw().getListOfParameters()
                for e in params:
                    if parameter.lower() in e.getId().lower():
                        e.setValue(e.getValue() * data[datainfo.index(reaction.getId())][column])
            else:
                if not reaction.getKineticLaw():
                    message = "Kinetic law is missing from reaction."
                    raise SBMLmodFault(message, "INTERNAL_ERROR")

                params = reaction.getKineticLaw().getListOfParameters()
                found = False
                for e in params:
                    if parameter.lower() in e.getId().lower():
                        found = True
                        break

                if found:
                    keysNotInData += 1
                    listKeysNotInData.append(reaction.getId())

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: {} of {}.'.format(keysNotInData, len(newmodel.getListOfReactions())))
            warnings.append('The reaction IDs not found are: {}'.format(' '.join(listKeysNotInData)))

        return newmodel, warnings


    # Takes a model and a list of metabolites and initial concentrations
    # Returns a new model with the new initial concentrations
    def editInitialConcentrations(self, document, data, datainfo, warnings, column):

        model = document.getModel()
        newmodel = model.clone()

        keysNotInModel = 0
        listKeysNotInModel = ''

        for key in datainfo:
            if newmodel.getSpecies(key) is not None:
                newmodel.getSpecies(key).setInitialConcentration(data[datainfo.index(key)][column])
            else:
                keysNotInModel += 1
                listKeysNotInModel = listKeysNotInModel + ', ' + key

        if keysNotInModel:
            warnings.append(str(keysNotInModel) +
                            " species from the data file are not found in the current model.")
            warnings.append( 'Unknown species:\n' + str( listKeysNotInModel[2:len( listKeysNotInModel )] ) )

        return newmodel, warnings


    def addKineticLawParameter(self, document, parameter, warnings, default_value=None, data=None, datainfo=None, column=0):

        model = document.getModel()
        newmodel = model.clone()

        keysNotInData = 0
        listKeysNotInData = ''

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
                keysNotInData = keysNotInData + 1
                listKeysNotInData = listKeysNotInData + ' ' + reaction.getId()

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: ' + str(keysNotInData) + ' of ' + str(len(newmodel.getListOfReactions())) + '. Default value: ' + str(default_value) + ' has been inserted to these reactions.')
            warnings.append('The reaction IDs not found are: ' + str(listKeysNotInData))

        return newmodel, warnings


    def addBounds(self, document, warnings, default_value=1000, data=None, datainfo=None, column=0):
        model = document.getModel()
        newmodel = model.clone()
        upper = 'UPPER_BOUND'
        lower = 'LOWER_BOUND'

        keysNotInData = 0
        listKeysNotInData = ''

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
                keysNotInData = keysNotInData + 1
                listKeysNotInData = listKeysNotInData + ' ' + reaction.getId()

        if keysNotInData:
            warnings.append('Number of reaction IDs not found in the data is: ' + str(keysNotInData) + ' of ' + str(len(newmodel.getListOfReactions())) + '. Default value: ' + str(default_value) + ' has been inserted to these reactions.')
            warnings.append('The reaction IDs not found are: ' + str(listKeysNotInData))

        return newmodel, warnings


    def replaceGlobalParameters(self, document, data, column, datainfo, warnings, header=True):
        model = document.getModel()
        newmodel = model.clone()

        for key in datainfo:
            if newmodel.getParameter(key) is not None:
                param = newmodel.getParameter(key)
                param.setValue(data[datainfo.index(key)][column])
            else:
                warnings.append(key + ' (GlobalParameter) not found in model')

        return newmodel, warnings


    def scaleGlobalParameters(self, document, data, column, datainfo, warnings, header=True):
        model = document.getModel()
        newmodel = model.clone()

        for key in datainfo:
            if newmodel.getParameter(key) is not None:
                param = newmodel.getParameter(key)
                oldval = param.getValue()
                param.setValue(oldval * data[datainfo.index(key)][column])
            else:
                warnings.append(key + ' (GlobalParameter) not found in model')

        return newmodel, warnings
