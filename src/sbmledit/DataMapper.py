'''
Created on 4 Nov 2010

@author: st08574
'''
from sbmledit.SBMLEditFault import SBMLEditFault

class DataMapper(object):

    def setup(self,mapping_string,expr_string,col=2):
        self.setup_mapping(mapping_string)
        self.setup_expr(expr_string,col)

    def setup_mapping(self,mapping_string,header=True):
        self.mapping={}

        lines = mapping_string.split('\n')

        lno = 0
        if header: start=1
        else: start=0

        for line in lines:
            if lno>=start:
                columns = line.split('\t')
                if len(columns)<2:
                    message='The mapping file must have 2 columns'
                    raise SBMLEditFault(message, "FILE_HANDLING_ERROR")
                key=columns[0].strip()
                value = columns[1].strip()
                if key not in self.mapping.keys():
                    self.mapping[key] = [value]
                else:
                    self.mapping[key].append(value)
            lno=lno+1

        return self.mapping


    def setup_expr(self,expr_string,col=2, header=True):

        self.expr={}
        col=col-1
        lines = expr_string.split('\n')

        lno = 0
        if header: start=1
        else: start=0

        for line in lines:
            if lno>=start:
                columns = line.split('\t')
                if col>=len(columns):
                    message='The data column index is outside the range of the number of columns in the data file.'
                    raise SBMLEditFault(message, "FILE_HANDLING_ERROR")

                key=columns[0].strip()
                value = columns[col].strip()
                if key not in self.expr.keys():
                    try:
                        self.expr[key] = float(value)
                    except:
                        message='A value in the data column cannot be converted to float: '+value
                        raise SBMLEditFault(message, "FILE_HANDLING_ERROR")

            lno=lno+1

        return self.expr

    def mapExpressionToEnzymes(self,mode='MAX'):
        warning = self.checkMapping(self.mapping, self.expr)

        if mode=='MAX':
            expressionmapping = self.maxExpression(self.mapping,self.expr)
            return expressionmapping,warning
        elif mode=='SUM':
            expressionmapping = self.sumExpression(self.mapping,self.expr)
            return expressionmapping,warning
        elif mode=='MIN':
            expressionmapping = self.minExpression(self.mapping,self.expr)
            return expressionmapping,warning
        elif mode=='MEAN':
            expressionmapping = self.meanExpression(self.mapping,self.expr)
            return expressionmapping,warning
        elif mode=='MEDIAN':
            expressionmapping = self.medianExpression(self.mapping,self.expr)
            return expressionmapping,warning
        else:
            message = "The merge mode parameter has not been set to a valid option. Valid options are: 'MAX','MIN','MEDIAN','MEAN' and'SUM'."
            raise SBMLEditFault(message, "INTERNAL_ERROR")


    def checkMapping(self,mapping,expr):

        warning=[]

        for item in mapping.itervalues():
            for i in item:
                if not expr.has_key(i):
                    warning.append('Make sure the ids in either the mapping file or the data file does not contain '"'"'.')
                    warning.append('Expression value not found for mapping file ID: '+str(i))

        return warning


    def sumExpression(self,mapping,expr):

        ret = {}

        for key in mapping:
            genes = mapping[key]
            sum=0
            for g in genes:
                if g in expr.keys():
                    sum = sum+expr[g]

            ret[key]=sum

        return ret

    def maxExpression(self, mapping,expr):
        ret = {}

        for key in mapping:
            genes = mapping[key]

            values=[]
            for g in genes:
                if g in expr.keys():
                    values.append(expr[g])
            if values:
                ret[key]=max(values)

        return ret

    def minExpression(self, mapping,expr):
        ret = {}

        for key in mapping:

            genes = mapping[key]

            values=[]
            for g in genes:
                if g in expr.keys():
                    values.append(expr[g])

            if values:
                ret[key]=min(values)

        return ret

    def meanExpression(self, mapping,expr):
        ret = {}

        for key in mapping:
            genes = mapping[key]
            sum=0
            count=0
            for g in genes:
                if g in expr.keys():
                    sum = sum+expr[g]
                    count=count+1

            if count:
                ret[key]=sum/count

        return ret

    def medianExpression(self, mapping,expr):
        ret = {}
        for key in mapping:
            genes = mapping[key]
            vals=[]
            for g in genes:
                if g in expr.keys():
                    vals.append(expr[g])

            if vals:
                vals.sort()

                if len(vals)%2:
                    ret[key] = vals[len(vals)/2]
                else:
                    ret[key] = (vals[(len(vals)/2)-1]+vals[len(vals)/2])/2



        return ret