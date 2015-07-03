import base64
import logging
import zlib

from suds.client import Client


def main():

    # url = 'http://www.ii.uib.no/~annes/SBMLEdit.wsdl'

    # url = 'file:///scratch/Home/siv3/st08574/esysbio/pysbmledit/src/sbmledit/SBMLEdit.wsdl'

    # url = 'file:///scratch/Home/siv3/st08574/esysbio/pysbmledit/src/sbmledit/SBMLEdit-0.1.2.wsdl'
    # url = 'http://cbu.bioinfo.no/wsdl-test/SBMLEdit-0.1.2.wsdl'
    url = 'http://cbu.bioinfo.no/wsdl/SBMLEdit-0.1.2.wsdl'
    # url = 'http://www.bccs.uni.no/~hakont/files/wsdl/sbml-edit/SBMLEdit-0.1.2.wsdl'


    client = Client(url, cache=None)
    # client.service['http://127.0.0.1:11000/sbmledit'].setlocation()

    print client

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)

    # path='/Home/siv3/st08574/phd/eSysbio/case-study_Ecoli/data'
    # mappingfile_lines = "".join(open(path+'/mapping.txt','r'))
    # datafile_lines = "".join(open(path+'/Rfiles/foldchange.txt','r'))

    # sbmlfile_lines = "".join(open(path+'/models/BIOMD0000000222.xml','r'))

    # sbmlfile_lines = "".join(open('../testsbmledit/resources/ValidSBML.xml','r'))
    # mappingfile_lines = "".join(open('../testsbmledit/resources/mapping.txt','r'))
    # datafile_lines = "".join(open('../testsbmledit/resources/expression_glu_ace_Oh_etal.dat','r'))
    # concfile_lines = "".join(open('../testsbmledit/resources/InitialConc_acetate.txt','r'))

    # path='/Home/siv3/st08574/phd/modellering/trpmet/expression/nature_cancer_case'
    path = '/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp'
    # path = '/scratch/Home/siv3/st08574/phd/svn/kinetic/NAD/'
    sbmlfile_lines = "".join(open(path + '/models/sbml/TRP_mammal_turnover_Oxy_GlobalParameters.xml', 'r'))
    # sbmlfile_lines = "".join(open(path+'/models/sbml/TRP_mammal_turnover_TyrosineCompetition.xml','r'))
    # sbmlfile_lines = "".join(open(path+'/models/sbml/Celegans_basemodel.xml','r'))
    # sbmlfile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/operationAutomatic/AutoCollectedKinetics2.xml','r'))
    # sbmlfile_lines = "".join(open(path+'NADmetabolismMerged.xml','r'))

    # path = '/Home/siv3/st08574/phd/svn.old/kinetic/Trp'
    # sbmlfile_lines = "".join(open(path+'/sbml/Trp_nokinetics.xml','r'))

    # sbmlfile_lines = "".join(open(path+'/models/oxygen/TRP_mammal_turnover_Oxy.xml','r'))
    # mappingfile_lines = "".join(open(path+'/mapping_rat.txt','r'))
    # mappingfile_lines = "".join(open(path+'/mapping_human.txt','r'))
    # mappingfile2_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/mappingRat_GlobalParameters.txt','r'))
    # mappingfile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/mapping_rat.txt','r'))
    # mappingfile2_lines = "".join(open('/scratch/Home/siv3/st08574/trp/JenAge/Celegans/mappingCE_GlobalParameters.txt','r'))
    # mappingfile_lines = "".join(open('/scratch/Home/siv3/st08574/trp/JenAge/Celegans/mapping_ce_ecnr.txt','r'))

    mappingfile2_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/mappingHum_GlobalParameters.txt', 'r'))
    mappingfile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/mapping_human.txt', 'r'))

    # path NAD:
    # #mappingfile2_lines = "".join(open(path+'/mappingHUM_globalparameters.txt','r'))
    # #mappingfile_lines = "".join(open(path+'/mappingHUM.txt','r'))

    # datafile_lines="".join(open(path+'TissueDatasetHUM.txt','r'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/expression/ABhumanBodyMap_TrpGenes.txt','r'))

    datafile_lines = "".join(open(path + '/Published_Datasets/TB/Dataset.txt', 'r'))

    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/trp/JenAge/Celegans/TrpGenes_ce33samples.txt','r'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/expression/RAT_TrimmedMeanSignal_EachTissue_Vs_PooledReference_Signal_Intensities.txt','r'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/Huntington_Q111_Q7/MeanData.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/Huntington_Q111_Q7/Dataset.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn.old/kinetic/Trp/Published_Datasets/cancer4/Dataset.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/AlzheimerApoE_E-GEOD-29652/Dataset.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/AlzheimerNeuro/DatasetNormalised.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/JenAge/mm-skin-Trp.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/cancer3/Dataset.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/parkinson/Dataset_Tyr.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/parkinson/JenAge/Dataset_JenAge_mousebrain_TrpTyr.txt'))
    # datafile_lines = "".join(open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/CerebralMalaria/Dataset_RMAprocessed.txt'))

    # concfile_lines = "".join(open(path+'/InitialConc_acetate.txt','r'))


    sbml = base64.b64encode(zlib.compress(sbmlfile_lines))
    mapping = base64.b64encode(zlib.compress(mappingfile_lines))
    mapping2 = base64.b64encode(zlib.compress(mappingfile2_lines))
    data = base64.b64encode(zlib.compress(datafile_lines))
    # conc = base64.b64encode(zlib.compress(concfile_lines))
    # import pdb;pdb.set_trace()
    # print 'Inputmodel: ',client.service.ValidateSBMLModel(sbml)

    # tmpsbml=client.service.ReplaceInitialConcentrationsOfSpecies(SbmlModelFile=sbml, DataFile=conc)
    # response=client.service.ScaleKineticLawParameter(ParameterId="Vf_", DataColumnNumber=3,MergeMode='MAX' ,SbmlModelFile=sbml, DataFile=data,MappingFile=mapping)
    # response=client.service.ScaleKineticLawParameter(ParameterId="Vr_", DataColumnNumber=3,MergeMode='MAX' ,SbmlModelFile=response.SbmlModelFile, DataFile=data,MappingFile=mapping)
    # datafile = open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/expression/RAT_TrimmedMeanSignal_EachTissue_Vs_PooledReference_Signal_Intensities.txt','r')

    # datafile=open('/scratch/Home/siv3/st08574/phd/modellering/trpmet/expression/ABhumanBodyMap_TrpGenes.txt','r')

    datafile = open(path + '/Published_Datasets/TB/Dataset.txt')
    # datafile = open('/Home/siv3/st08574/phd/modellering/trpmet/expression/nature_cancer_case/Trp_natureCancerStudy_preprosessert.txt')
    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/Huntington_Q111_Q7/Dataset.txt')
    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/AlzheimerNeuro/DatasetNormalised.txt')
    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/cancer3/Dataset.txt')
    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/parkinson/Dataset_Tyr.txt')
    # datafile = open('/Home/siv3/st08574/phd/modellering/trpmet/expression/RAT_TrimmedMeanSignal_EachTissue_Vs_PooledReference_Signal_Intensities.txt')
    # datafile = open('/scratch/Home/siv3/st08574/trp/JenAge/Celegans/TrpGenes_ce33samples.txt')
    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/parkinson/JenAge/Dataset_JenAge_mousebrain_TrpTyr.txt')
    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/CerebralMalaria/Dataset_RMAprocessed.txt')

    # datafile = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/JenAge/mm-skin-Trp.txt')

    # datafile = open(path+'/Rfiles/foldchange.txt','r')
    # datafile = open(path+'TissueDatasetHUM.txt','r')

    # response = client.service.ReplaceGlobalParameters(DataColumnNumber=13,SbmlModelFile=sbml, DataFile=data,MappingFile=mapping2)
    # print 'Outputmodel: ',client.service.ValidateSBMLModel(SbmlModelFile=response.SbmlModelFile)
    # response=client.service.ReplaceKineticLawParameter(ParameterId="E_T", DataColumnNumber=13,MergeMode='MAX' ,SbmlModelFile=response.SbmlModelFile, DataFile=data,MappingFile=mapping)
    # print 'Outputmodel2: ',client.service.ValidateSBMLModel(SbmlModelFile=response.SbmlModelFile)

    lines = datafile.readlines()

    headers = lines[0].split('\t')
    # output=open(path+headers[13]+'Model.xml','w')
    # newsbml_filelines = zlib.decompress(base64.b64decode(response.SbmlModelFile))
    # output.write(newsbml_filelines)
    # output.close()
    # print len(headers)
    for i in range(2, len(headers) + 1):

        response = client.service.ReplaceGlobalParameters(DataColumnNumber=i, SbmlModelFile=sbml, DataFile=data, MappingFile=mapping2)
        response = client.service.ReplaceKineticLawParameter(ParameterId="E_T", DataColumnNumber=i, MergeMode='MAX' , SbmlModelFile=response.SbmlModelFile, DataFile=data, MappingFile=mapping)
        # response = client.service.ScaleKineticLawParameter(ParameterId="Vr",DataColumnNumber=i,SbmlModelFile=sbml, DataFile=data,MappingFile=mapping)
        # response = client.service.ScaleKineticLawParameter(ParameterId="Vf",DataColumnNumber=i,SbmlModelFile=response.SbmlModelFile, DataFile=data,MappingFile=mapping)

        # response = client.service.AddBoundsToKineticLaw(DataColumnNumber=i,SbmlModelFile=sbml, DataFile=data,MappingFile=mapping2)

        output = open(path + '/Published_Datasets/TB/models/' + headers[i - 1].strip() + '.xml', 'w')

        # output=open('/scratch/Home/siv3/st08574/trp/models/tissues/globalparams/'+headers[i-1]+'_RAT_GlobalParams.xml','w')

        # output=open('/scratch/Home/siv3/st08574/trp/models/tissues/globalparams/'+headers[i-1]+'_HUM_GlobalParams.xml','w')

        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/Huntington_Q111_Q7/'+headers[i-1]+'_HumanGlobalParams.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn.old/kinetic/Trp/Published_Datasets/cancer4/models/'+headers[i-1].strip()+'_'+str(i-1)+'_HumanGlobalParams.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn.old/kinetic/Trp/FBA/models/'+headers[i-1].strip()+'_'+str(i-1)+'_bounds.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/AlzheimerApoE_E-GEOD-29652/models/'+headers[i-1].strip()+'_'+str(i-1)+'_HumanGlobalParams.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/AlzheimerNeuro/models/'+headers[i-1].strip()+'_'+str(i-1)+'_HumanGlobalParams.xml','w')
        # output=open(path+'/models/'+headers[i-1].strip()+'_ecoli.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/cancer3/models/'+headers[i-1].strip()+'_'+str(i-1)+'_HumanGlobalParams.xml','w')
        # output = open('/scratch/Home/siv3/st08574/phd/modellering/operationAutomatic/models/'+headers[i-1].strip()+'_'+str(i-1)+'.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/JenAge/mm-skin/mm-skin-'+headers[i-1].strip()+'.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/JenAge/Celegans/models/ce-'+headers[i-1].strip()+'.xml','w')

        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/parkinson/models/models_Tyr/'+headers[i-1].strip()+'_'+str(i-1)+'_HumanGlobalParams.xml','w')
        # output=open('/scratch/Home/siv3/st08574/phd/svn/kinetic/parkinson/JenAge/models/'+headers[i-1].strip()+'_'+str(i-1)+'_mousebrain.xml','w')
        # output = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/CerebralMalaria/models/'+headers[i-1].strip()+'_'+str(i-1)+'_HumanGlobalParams.xml','w')
        newsbml_filelines = zlib.decompress(base64.b64decode(response.SbmlModelFile))
        output.write(newsbml_filelines)
        output.close()

        # try:
        #    warnings=response.Warnings
            # output = open(path+'/Warnings.txt','w')
            # output = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/parkinson/JenAge/models/Warnings.txt','w')
        #    output = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/CerebralMalaria/Warnings.txt','w')
        #    output.write('\n'.join(warnings))
        #    output.close()
        # except:
        #    pass

    # print 'Outputmodel: ',client.service.ValidateSBMLModel(SbmlModelFile=response.SbmlModelFile)

    # response = client.service.ReplaceGlobalParameters(DataColumnNumber=31,SbmlModelFile=sbml, DataFile=data,MappingFile=mapping2)

    # response=client.service.ReplaceKineticLawParameter(ParameterId="E_T", DataColumnNumber=31,SbmlModelFile=response.SbmlModelFile, DataFile=data,MappingFile=mapping)
    # newsbml_filelines = zlib.decompress(base64.b64decode(response.SbmlModelFile))

    # output = open(path+'/models/oxygen/rat/'+headers[i]+'.xml','w')
    # output=open(path+'/sensitivity_analysis/Liver_TRP_mammal_turnover_Oxy_GlobalParameters.xml','w')
    # output.write(newsbml_filelines)
    # output.close()

    try:
        warnings = response.Warnings
        output = open(path + '/Warnings.txt', 'w')
        # output = open('/scratch/Home/siv3/st08574/phd/svn/kinetic/Trp/Published_Datasets/parkinson/models/models_Tyr/Warnings.txt','w')
        output.write('\n'.join(warnings))
        output.close()
    except:
        pass


if __name__ == '__main__':
    main()
