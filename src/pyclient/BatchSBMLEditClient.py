from suds.client import Client
import logging
import zlib
import base64

def main():


    url = 'file:///scratch/Home/siv3/st08574/esysbio/pysbmledit/src/sbmledit/SBMLEdit_batchmode.wsdl'
    #url = 'file:///scratch/Home/siv3/st08574/esysbio/pysbmledit/src/sbmledit/SBMLedit.wsdl'

    client = Client(url, cache=None)
    #client.service['http://127.0.0.1:11000/sbmledit'].setlocation()

    print client



    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.CRITICAL)

    print 'version: ', client.service.GetVersion()
    #print 'Are you alive ?', client.service.Alive()

    print 'reading files'

    sbmlfile_lines = "".join(open('../testsbmledit/resources/TRP_mammal_turnover_Oxy_GlobalParameters.xml','r'))
    mappingfile_lines = "".join(open('../testsbmledit/resources/mapping_applied_rat.txt','r'))
    mappingfile2_lines = "".join(open('../testsbmledit/resources/mappingRat_GlobalParameters.txt','r'))
    datafile_lines = "".join(open('../testsbmledit/resources/RotteBiweightAlleVev.txt','r'))
    #datafile_lines = "".join(open('../testsbmledit/resources/TestingAvGenuttryksformater.csv','r'))
    #concfile_lines = "".join(open('../testsbmledit/resources/InitialConc_acetate.txt','r'))

    #sbmlfile_lines = "".join(open('../testsbmledit/resources/SBMLwithoutKinetics.xml','r'))
    #mappingfile_lines = "".join(open('../testsbmledit/resources/mapping.txt','r'))
    #datafile_lines = "".join(open('../testsbmledit/resources/expression_glu_ace_Oh_etal.dat','r'))
    #datafile_lines = "".join(open('../testsbmledit/resources/InitialConc_acetate.txt','r'))

#    sbmlfile_lines = "".join(open('../testsbmledit/resources/SimplifiedModel2.xml','r'))
#    mappingfile_lines = "".join(open('../testsbmledit/resources/mappingNeisseria.txt','r'))
#    datafile_lines = "".join(open('../testsbmledit/resources/RNAseq_M58_a522.txt','r'))


    sbml = base64.b64encode(zlib.compress(sbmlfile_lines))
    mapping = base64.b64encode(zlib.compress(mappingfile_lines))
    mapping2 = base64.b64encode(zlib.compress(mappingfile2_lines))
    data = base64.b64encode(zlib.compress(datafile_lines))

    sbmle = base64.b64encode(sbmlfile_lines)
    mappinge = base64.b64encode(mappingfile_lines)
    mapping2e = base64.b64encode(mappingfile2_lines)
    datae = base64.b64encode(datafile_lines)

    sbml_files=[]
    sbml_files.append(sbml)
    sbml_files.append(sbml)
    sbml_files.append(sbml)
#    sbml_files.append(sbml)
#    sbml_files.append(sbml)
#    sbml_files.append(sbml)
#    sbml_files.append(sbml)
    print 'sending request'

    response = client.service.ValidateSBMLModelGzippedBase64Encoded(SbmlModelFile=sbml)
    #response = client.service.ValidateSBMLModelText(SbmlModelFile=sbmlfile_lines)
    #response = client.service.ValidateSBMLModelBase64Encoded(SbmlModelFile=sbmle)

    print 'ModelIsValid:',response.ModelIsValid


    #response = client.service.ReplaceGlobalParametersGzippedBase64Encoded(SbmlModelFiles=sbml, DataFile=data,ParameterId="E_T",DataColumnNumber=3,MappingFile=mapping,BatchMode=False)
    #response = client.service.ReplaceGlobalParametersText(SbmlModelFiles=sbmlfile_lines, DataFile=datafile_lines,ParameterId="E_T",DataColumnNumber=3,MappingFile=mappingfile_lines,BatchMode=False)
    #response = client.service.ReplaceGlobalParametersBase64Encoded(SbmlModelFiles=sbmle, DataFile=datae,ParameterId="E_T",DataColumnNumbere=3,MappingFile=mappinge,BatchMode=False)

    #response = client.service.ScaleGlobalParametersGzippedBase64Encoded(SbmlModelFiles=sbml, DataFile=data,DataColumnNumber=3,MappingFile=mapping2,BatchMode=False)
    #response = client.service.ScaleGlobalParametersText(SbmlModelFiles=sbmlfile_lines, DataFile=datafile_lines,DataColumnNumber=3,MappingFile=mappingfile2_lines,BatchMode=False)
    #response = client.service.ScaleGlobalParametersBase64Encoded(SbmlModelFiles=sbmle, DataFile=datae,DataColumnNumber=3,MappingFile=mapping2e,BatchMode=False)

    #response = client.service.ScaleKineticLawParameterBase64Encoded(SbmlModelFiles=sbmle, DataFile=datae,ParameterId="E_T",DataColumnNumber=2,MappingFile=mappinge,BatchMode=False)
    #response = client.service.ScaleKineticLawParameterGzippedBase64Encoded(SbmlModelFiles=sbml, DataFile=data,ParameterId="E_T",DataColumnNumber=2,MappingFile=mapping,BatchMode=False)
    #response = client.service.ScaleKineticLawParameterText(SbmlModelFiles=sbmlfile_lines, DataFile=datafile_lines,ParameterId="E_T",DataColumnNumber=2,MappingFile=mappingfile_lines,BatchMode=False)


    #response = client.service.ReplaceKineticLawParameter(SbmlModelFiles=sbml, DataFile=data,ParameterId="E_T",DataColumnNumber=2,MappingFile=mapping,BatchMode=False)
    #response = client.service.ReplaceKineticLawParameterBase64Encoded(SbmlModelFiles=sbmle, DataFile=datae,ParameterId="E_T",DataColumnNumber=2,MappingFile=mappinge,BatchMode=False)
    #response = client.service.ReplaceKineticLawParameterGzippedBase64Encoded(SbmlModelFiles=sbml, DataFile=data,ParameterId="E_T",DataColumnNumber=2,MappingFile=mapping,BatchMode=False)
    #response = client.service.ReplaceKineticLawParameterText(SbmlModelFiles=sbmlfile_lines, DataFile=datafile_lines,ParameterId="E_T",DataColumnNumber=2,MappingFile=mappingfile_lines,BatchMode=False)

    #response = client.service.AddBoundsToKineticLawText(SbmlModelFiles=sbmlfile_lines,DataFile = datafile_lines,DefaultValue=999, DataColumnNumber=10, MappingFile=mappingfile_lines,BatchMode=False)
    #response = client.service.AddBoundsToKineticLawBase64Encoded(SbmlModelFiles=sbmle,DataFile = datae,DefaultValue=999, DataColumnNumber=10, MappingFile=mappinge,BatchMode=False)
    #response = client.service.AddBoundsToKineticLawGzippedBase64Encoded(SbmlModelFiles=sbml,DataFile = data,DefaultValue=999, DataColumnNumber=3, MappingFile=mapping,BatchMode=False)
    #response = client.service.AddBoundsToKineticLaw(SbmlModelFiles=sbml,DataFile = data,DefaultValue=999, DataColumnNumber=3, MappingFile=mapping,BatchMode=False)
    #response = client.service.AddBoundsToKineticLawText(SbmlModelFiles=sbmlfile_lines,DefaultValue=999, BatchMode=False)


    #response = client.service.AddKineticLawParameter(SbmlModelFiles=sbml_files,ParameterId="Upper",DataFile = data,DefaultValue=999, DataColumnNumber=10, MappingFile=mapping,BatchMode=True)
    #response = client.service.ReplaceInitialConcentrationsOfSpecies(SbmlModelFiles=sbml_files,DataFile = data,DefaultValue=2.5,BatchMode=True)
    #response = client.service.ReplaceInitialConcentrationsOfSpecies(SbmlModelFiles=sbml,DataFile = data,DefaultValue=2.5,BatchMode=False)

#    files=[]
#    for file in response.SbmlModelFiles:
#        files.append(file.SbmlModelFile)
#
#    response = client.service.ReplaceKineticLawParameter(SbmlModelFiles=files, DataFile=data,ParameterId="E_T",MappingFile=mapping,BatchMode=True)

#    files=[]
#    for file in response.SbmlModelFiles:
#        files.append(file.SbmlModelFile)
#
#    response = client.service.ReplaceGlobalParameters(SbmlModelFiles=files, DataFile=data,ParameterId="E_T",MappingFile=mapping2,BatchMode=True)
#    #response = client.service.ScaleKineticLawParameter(SbmlModelFiles=sbml_files, DataFile=data,ParameterId="E_T",MappingFile=mapping2,BatchMode=True)

#
#    newsbml_files = response.SbmlModelFiles
#    print 'Antall sbml files i retur: ',len(newsbml_files)
#
#    print 'writing output'
#    i=0
#    for file in newsbml_files:
#        name='NEW'
#        if file.Name:
#            name = file.Name
#        #resultat = base64.b64decode(file.SbmlModelFile)
#        #resultat = zlib.decompress(base64.b64decode(file.SbmlModelFile))
#        resultat = file.SbmlModelFile
#        output = open('../testsbmledit/resources/models/'+name+'.xml','w')
#        output.write(resultat)
#        output.close()
#        i+=1


#
#
#    try:
#        warnings=response.Warnings
#        output = open('../testsbmledit/resources/models/Warnings.txt','w')
#        #output = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/parkinson/models/models_Tyr/Warnings.txt','w')
#        output.write('\n'.join(warnings))
#        output.close()
#    except:
#        pass


if __name__ == '__main__':
    main()
