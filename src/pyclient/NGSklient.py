from suds.client import Client
import logging
import zlib
import base64

def main():

    url = 'http://www.ii.uib.no/~annes/SBMLEdit.wsdl'
    client = Client(url, cache=None)
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)

    path = '/scratch/Home/siv3/st08574/phd/eSysbio/case-study_NeisseriaMeningitidis/'
    #sbmlfile_lines = "".join(open(path+'data/models/SimplifiedModel2.xml','r'))
    #sbmlfile_lines = "".join(open(path+'data/models/SimplifiedModelPlus.xml','r'))
    sbmlfile_lines = "".join(open(path+'data/models/SimplifiedModelPlusDenitrification.xml','r'))
    mappingfile_lines = "".join(open(path+'data/mappingfile.txt','r'))
    datafile_lines = "".join(open(path+'data/NMtable.unfiltered_Ids_in_first_column.csv','r')) #NGS data
    #datafile_lines = "".join(open(path+'data/expression/Microarray_biweight_data_tab_delim.txt','r')) # Microarray data


    sbml = base64.b64encode(zlib.compress(sbmlfile_lines))
    mapping = base64.b64encode(zlib.compress(mappingfile_lines))
    data = base64.b64encode(zlib.compress(datafile_lines))

    valid = client.service.ValidateSBMLModel(sbml)
    if valid:
        print 'sbml is valid'
    else:
        print 'sbml is NOT valid'

    #newsbml = client.service.AddKineticLawParameter(sbml,"OBJECTIVE_COEFFICIENT",DataColumnNumber=8,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #print newsbml
    #newsbml = client.service.AddKineticLawParameter(sbml,'UPPER',1000)

    pathout='models_with_limits/SimplifiedModelPlusDinitrification/NGS/'

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=4,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=7,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_MC58.PPM.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_MC58_PPM.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=8,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=9,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_MC58.Saliva.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_MC58_Saliva.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=12,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=6,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_MC58.Blood.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_MC58_Blood.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=16,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=8,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_MC58.CSF.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_MC58_CSF.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    datafile_lines = "".join(open(path+'data/a522.txt','r'))
    data = base64.b64encode(zlib.compress(datafile_lines))


    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=4,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=3,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_a522.PPM.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_a522_PPM.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=8,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=5,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_a522.Saliva.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_a522_Saliva.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=12,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=2,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_a522.Blood.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_a522_Blood.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()

    newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1,DataColumnNumber=16,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    #newsbml = client.service.AddBoundsToKineticLaw(sbml,DefaultValue=1000,DataColumnNumber=4,MergeMode='MIN',MappingFile=mapping,DataFile=data)
    newsbml_filelines = zlib.decompress(base64.b64decode(newsbml.SbmlModelFile))
    #output = open(path+pathout+'SimplifiedModelPlus_a522.CSF.RPKM_withLimits.xml','w')
    output = open(path+pathout+'SimplifiedModelPlusDenitrification_NGS_a522_CSF.UQN_withLimits.xml','w')
    output.write(newsbml_filelines)
    output.close()



    try:
        warnings=newsbml.Warnings
        output = open(path+'Warnings.txt','w')
        output.write('\n'.join(warnings))
        output.close()
    except:
        pass


if __name__ == '__main__':
    main()