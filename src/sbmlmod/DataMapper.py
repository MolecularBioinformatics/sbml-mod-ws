from sbmlmod.SBMLmod_fault import SBMLmodFault


class DataMapper(object):

    def setup(self, mapping_string, expr_string, col=2, header=True, batch=False):
        self.setup_mapping(mapping_string)
        self.setup_expr(expr_string, col, header, batch)


    def setup_mapping(self, mapping_string, header=True):
        self.mapping = {}
        self.iso = []
        self.complex = []

        lines = mapping_string.split('\n')

        lno = 0
        if header: start = 1
        else: start = 0

        for line in lines:
            if lno >= start:
                columns = line.split('\t')
                if len(columns) < 2:
                    message = 'The mapping file must have at least 2 columns'
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                key = columns[0].strip()
                value = columns[1].strip()
                if key not in self.mapping.keys():
                    self.mapping[key] = [value]
                else:
                    self.mapping[key].append(value)

                if len(columns) == 3:
                    if columns[2].strip() == 'ISO':
                        self.iso.append(columns[0])
                    elif columns[2].strip() == 'COMPLEX':
                        self.complex.append(columns[0])

            lno = lno + 1

        ret = self.mapping

        return ret


    def setup_expr(self, expr_string, col=2, header=True, batch=False):
        if expr_string is not None:
            lines = expr_string.split('\n')
            lineLength = len(lines[0].split('\t'))
        else:
            lineLength = -1

        if col > lineLength:
            message = 'The data column index is outside the range of the number of columns in the data file.'
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        self.exprId = []

        lno = 0
        if header:
            start = 1
        else:
            start = 0

        # self.expr=[[0 for x in xrange(rows)] for x in xrange(cols)]
        self.expr = []

        col = col - 1

        for line in lines:
            if lno >= start:
                newrow = []
                columns = line.split('\t')
                if len(columns) != lineLength:
                    message = 'Columns are of unequal length'
                    raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                self.exprId.append(columns[0].strip())
                if batch:
                    for i in range(col, len(columns)):
                        try:
                            newrow.append(float(columns[i]))
                        except:
                            message = 'A value in the data column cannot be converted to float: ' + columns[i]
                            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                else:
                    try:
                        newrow.append(float(columns[col]))
                    except:
                        message = 'A value in the data column cannot be converted to float: ' + columns[col]
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")
                self.expr.append(newrow)

            lno = lno + 1

        return self.expr , self.exprId


    def mergeExpressionValuesMappingToSameReaction(self, mode='MAX', warning=[]):
        warning = self.checkMapping(self.mapping, self.exprId, warning)

        if mode == 'MAX':
            self.maxExpression(self.mapping, self.expr, self.exprId)
            return self.expr, self.exprId, warning
        elif mode == 'SUM':
            self.sumExpression(self.mapping, self.expr, self.exprId)
            return self.expr, self.exprId, warning
        elif mode == 'MIN':
            self.minExpression(self.mapping, self.expr, self.exprId)
            return self.expr, self.exprId, warning
        elif mode == 'MEAN':
            self.meanExpression(self.mapping, self.expr, self.exprId)
            return self.expr, self.exprId, warning
        elif mode == 'MEDIAN':
            self.medianExpression(self.mapping, self.expr, self.exprId)
            return self.expr, self.exprId, warning
        elif mode == 'E-FLUX':
            self.eFlux(self.mapping, self.expr, self.exprId)
            return self.expr, self.exprId, warning
        else:
            message = "The merge mode parameter has not been set to a valid option. Valid options are: 'MAX','MIN','MEDIAN','MEAN' and'SUM'."
            raise SBMLmodFault(message, "INTERNAL_ERROR")


    def checkMapping(self, mapping, exprId, warning=[]):
        missingExpr = []
        noMissing = 0
        total = 0
        for item in mapping.itervalues():
            total += len(item)
            for i in item:
                if i not in exprId:
                    missingExpr.append(i)
                    noMissing += 1

        if missingExpr:
            warning.append("Checking Mapping...")
            if noMissing == total:
                message = "None of the reaction id's can be found in the dataset."
                raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

            warning.append(str(noMissing) + ' of ' + str(total) + " of reaction id's from the mapping file are not found in the dataset.")
            warning.append('Expression value not found for: ' + str(missingExpr))
            warning.append('Make sure the ids in either the mapping file or the data file does not contain quotation marks.')

        return warning


    def sumExpression(self, mapping, expr, geneNames):
        mergeExpression = []
        mergeExprId = []

        for key in mapping:
            genes = mapping[key]
            if len(genes) > 1:
                newrow = []
                for i in range(len(expr[0])):
                    sum = 0
                    for g in genes:
                        if g in geneNames:
                            sum = sum + expr[geneNames.index(g)][i]

                    if sum:
                        newrow.append(sum)

                mergeExpression.append(newrow)
                mergeExprId.append(key)
            else:
                if genes[0] in geneNames:
                    mergeExpression.append(expr[geneNames.index(genes[0])])
                    mergeExprId.append(key)

        self.expr = mergeExpression
        self.exprId = mergeExprId

        return mergeExpression, mergeExprId


    def maxExpression(self, mapping, expr, geneNames):
        mergeExpression = []
        mergeExprId = []

        for key in mapping:
            genes = mapping[key]
            if len(genes) > 1:
                newrow = []
                for i in range(len(expr[0])):
                    values = []
                    for g in genes:
                        if g in geneNames:
                            values.append(expr[geneNames.index(g)][i])

                    if values:
                        newrow.append(max(values))

                mergeExpression.append(newrow)
                mergeExprId.append(key)
            else:
                if genes[0] in geneNames:
                    mergeExpression.append(expr[geneNames.index(genes[0])])
                    mergeExprId.append(key)

        self.expr = mergeExpression
        self.exprId = mergeExprId

        return mergeExpression, mergeExprId


    def minExpression(self, mapping, expr, geneNames):
        mergeExpression = []
        mergeExprId = []

        for key in mapping:
            genes = mapping[key]
            if len(genes) > 1:
                newrow = []
                for i in range(len(expr[0])):
                    values = []
                    for g in genes:
                        if g in geneNames:
                            values.append(expr[geneNames.index(g)][i])

                    if values:
                        newrow.append(min(values))

                mergeExpression.append(newrow)
                mergeExprId.append(key)
            else:
                if genes[0] in geneNames:
                    mergeExpression.append(expr[geneNames.index(genes[0])])
                    mergeExprId.append(key)

        self.expr = mergeExpression
        self.exprId = mergeExprId

        return mergeExpression, mergeExprId


    def meanExpression(self, mapping, expr, geneNames):
        mergeExpression = []
        mergeExprId = []

        for key in mapping:
            genes = mapping[key]
            if len(genes) > 1:
                newrow = []
                for i in range(len(expr[0])):
                    count = 0
                    sum = 0
                    for g in genes:
                        if g in geneNames:
                            sum = sum + expr[geneNames.index(g)][i]
                            count = count + 1

                    if sum and count:
                        newrow.append(sum / count)

                mergeExpression.append(newrow)
                mergeExprId.append(key)
            else:
                if genes[0] in geneNames:
                    mergeExpression.append(expr[geneNames.index(genes[0])])
                    mergeExprId.append(key)

        self.expr = mergeExpression
        self.exprId = mergeExprId

        return mergeExpression, mergeExprId


    def medianExpression(self, mapping, expr, geneNames):
        mergeExpression = []
        mergeExprId = []

        for key in mapping:
            genes = mapping[key]
            if len(genes) > 1:
                newrow = []
                for i in range(len(expr[0])):
                    values = []
                    for g in genes:
                        if g in geneNames:
                            values.append(expr[geneNames.index(g)][i])

                    if values:
                        values.sort()

                    if len(values) % 2:
                        val = values[len(values) / 2]
                    else:
                        val = (values[(len(values) / 2) - 1] + values[len(values) / 2]) / 2

                    if val:
                        newrow.append(val)

                mergeExpression.append(newrow)
                mergeExprId.append(key)
            else:
                if genes[0] in geneNames:
                    mergeExpression.append(expr[geneNames.index(genes[0])])
                    mergeExprId.append(key)

        self.expr = mergeExpression
        self.exprId = mergeExprId

        return mergeExpression, mergeExprId


    def eFlux(self, mapping, expr, geneNames):
        mergeExpression = []
        mergeExprId = []

        if not self.iso and not self.complex:
            message = 'To use E-FLUX a third column must be specified in the mapping file marking genes that contributes to enzyme complexes and/or iso-enzymes. Annotation should be "COMPLEX" and "ISO" respectively.'
            raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

        for key in mapping:
            genes = mapping[key]
            if len(genes) > 1:
                newrow = []
                for i in range(len(expr[0])):
                    values = []
                    for g in genes:
                        if g in geneNames:
                            values.append(expr[geneNames.index(g)][i])

                    if key in self.iso:
                        val = sum(values)
                    elif key in self.complex:
                        val = min(values)
                    else:
                        message = 'More than one gene maps to the enzyme ' + key + ', however the genes are not annotated with "COMPLEX" or "ISO" in the mapping file'
                        raise SBMLmodFault(message, "FILE_HANDLING_ERROR")

                    if val:
                        newrow.append(val)

                mergeExpression.append(newrow)
                mergeExprId.append(key)
            else:
                if genes[0] in geneNames:
                    mergeExpression.append(expr[geneNames.index(genes[0])])
                    mergeExprId.append(key)

        self.expr = mergeExpression
        self.exprId = mergeExprId

        return mergeExpression, mergeExprId
