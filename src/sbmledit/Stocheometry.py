


class Stocheometry(object):
    '''
    classdocs
    '''


    def calculateStocheometryMatrix(self,document):
        self.stochmatrix=[]

        model = document.getModel()
        reactions = model.getListOfReactions()
        species = model.getListOfSpecies()

        for s in species:
            name=s.getId()
            stoch=[]
            for r in reactions:
                reactants=r.getListOfReactants()
                products=r.getListOfProducts()

                set=False

                for rf in reactants:
                    if name == rf.getSpecies():
                        stoch.append(-1)
                        set=True

                for rf in products:
                    if name == rf.getSpecies():
                        stoch.append(1)
                        set=True

                if not set:
                    stoch.append(0)

            self.stochmatrix.append(stoch)

    def getStocheometryMatrix(self):
        return self.stochmatrix

    def setSpeciesExtOrInt(self,document, stochmatrix):

        model=document.getModel()
        newmodel=model.clone()

        species = newmodel.getListOfSpecies()

        for i in range(1,len(species)):
            reac=False
            prod=False

            for val in stochmatrix[i]:
                if val==1:
                    prod=True
                elif val == -1:
                    reac=True

            if prod and reac:
                species[i].setBoundaryCondition(False)
            else:
                species[i].setBoundaryCondition(True)
                species[i].setConstant(True)

        return newmodel




