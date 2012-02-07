"""
Note most of this is copied from AUREA.GUI.Controller.
"""
from AUREA.learner import ktsp, tst, dirac, tsp
from AUREA.parser import SOFTParser, GMTParser, SettingsParser, CSVParser
from AUREA.packager import DataCleaner, DataPackager
from AUREA.heuristic import ResourceEstimate, LearnerQueue
import os
import json
import cPickle as pickle

from optparse import OptionParser

def runAUREA(options):
    dp=getData(options)
    learner=getLearner(options)
    config=getConfig(options)


    #pickle.dump(dp, pickle_file)
    #dp = pickle.load(pickle_file)
    #pickle_file.close()
    trained_learner = None
    if learner == 'tsp':
        """ removed pickling
        #print dp.probes
        if False: 
            trained_learner = trainTSP( dp, config)
            pickle_file = open("tsp.pkl", 'wb')
            pickle.dump(trained_learner, pickle_file)
            pickle_file.close()
        else:
            pickle_files = open("tsp.pkl", 'rb')
            trained_learner = pickle.load(pickle_files)
            pickle_files.close()
        #print dp.probes
        """
        trained_learner = trainTSP( dp, config)
        return extractTSP(dp, config, trained_learner)
    elif learner == 'tst':
        trained_learner = trainTST( dp, config)
        return extractTST(dp, config, trained_learner)
    elif learner == 'ktsp':
        trained_learner = trainkTSP(dp, config)
        return extractkTSP(dp, config, trained_learner)
    elif learner == 'dirac':
        trained_learner = trainDIRAC(dp, config)

def getConfig(options):
    config_file=options.config_file
    if not os.path.isfile(str(config_file)):
        raise Exception("ERROR: config file ["+ str(config_file)  + "] does not exist\n")
    config = SettingsParser.SettingsParser(config_file)
    return config

def getLearner(options):
    valid_learners =  ['tsp', 'tst', 'ktsp', 'dirac', 'adaptive']
    learner=options.learner
    if learner not in valid_learners:
        err =  "ERROR: " + str(learner) + " is not a valid learner.\n"
        err +=  "\tvalid options are [" + " ".join(valid_learners) + "]\n"
        raise Exception(err)
    return learner

def getData(options):
    if hasattr(options, 'input_file_one') and hasattr(options, 'input_file_two'):
        file1=options.input_file_one
        file2=options.input_file_two
        return getCsvData(file1, file2)

    if hasattr(options, 'pheno1'):
        return getPhenoData(options.pheno1, options.pheno2)

    raise Exception(options.usage)



def getCsvData(in1, in2):
    #check inputs
    resultString = ""
    if not os.path.isfile(str(in1)):
        resultString += "ERROR: input table 1["+ str(in1)  + "] does not exist\n"
    if not os.path.isfile(str(in2)):
        resultString += "ERROR: input table 2["+ str(in2)  + "] does not exist\n"

    if len(resultString) > 0:
        raise Exception(resultString)
    #pickle_file = open("datapackage2.pkl ", 'rb')

    dp = buildCsvData(in1, in2, config)
    return dp

def buildCsvData(file1, file2, config):
    """
    Takes the 2 csv file names and the config object and returns the datapackage
    """
    gnffile=config.getSetting('datatable', 'gnfile')[0]
    synfile=config.getSetting('datatable','synfile')[0]
>>>>>>> b10d420723b3a8dd35495e037303f1abb9800672:scripts/testScripts/aurea.v.py

    collision = config.getSetting("datatable", "Gene Collision Rule")[0]
    bad_data = config.getSetting("datatable", "Bad Data Value")[0]
    gene_column = config.getSetting("datatable", "Gene Column")[0]
    probe_column = config.getSetting("datatable", "Probe Column")[0]

    gnf = GMTParser.GMTParser(gnfile)
    #VC: edit here
    #create GEO Data Getter
    #f1=GEODataGetter()

    f1 = CSVParser.CSVParser(file1, probe_column_name=probe_column, gene_column_name=gene_column)
    f2 = CSVParser.CSVParser(file2, probe_column_name=probe_column, gene_column_name=gene_column)
    #create a data table
    dt1 = DataCleaner.DataTable(probe_column, gene_column, collision, bad_data)
    dt1.getCSVData(f1)
    dt2 = DataCleaner.DataTable(probe_column, gene_column, collision, bad_data)
    dt2.getCSVData(f2)
    #VC: done edit
    
    dp = DataPackager.dataPackager(merge_cache=".")
    dp.addGeneNetwork(gnf.getAllNetworks())
    dp.addSynonyms(synfile)
    #add data table
    dp.addDataTable(dt1)
    dp.addDataTable(dt2)
    

    #create subsets(classes)
    dp.createClassification("f1")
    for samp in f1.getDataColumnHeadings():
        dp.addToClassification("f1", dt1.dt_id, samp)
    dp.createClassification("f2")
    for samp in f2.getDataColumnHeadings():
        dp.addToClassification("f2", dt2.dt_id, samp)
    return dp


def getPhenoData(pheno1, pheno2=None, config):
    collision = config.getSetting("datatable", "Gene Collision Rule")[0]
    bad_data = config.getSetting("datatable", "Bad Data Value")[0]
    gene_column = config.getSetting("datatable", "Gene Column")[0]
    probe_column = config.getSetting("datatable", "Probe Column")[0]
    gnffile=config.getSetting('datatable', 'gnfile')[0]
    synfile=config.getSetting('datatable','synfile')[0]

    gdd1=GEODataGetter(pheno1)
    geo_ids=GEO.GEOBase.ids_with_pheno(pheno1)
    for geo_id in geo_ids:
        gdd1.add_geo_id(geo_id)
    dt1=DataCleaner.DataTable(probe_column, gene_column, collision, bad_data)
    dt1.getGEOData(gdd1)

    if pheno2:
        gdd2=GEODataGetter(pheno2)
        geo_ids=GEO.GEOBase.GEOBase.ids_with_pheno(pheno2)
        for geo_id in geo_ids:
            gdd2.add_geo_id(geo_id)
    else:
        pheno2='not '+pheno1
        gdd2=GEODataGetter(pheno2)
        sample_ids=GEO.Sample.Sample.all_ids(id_type='probe')
        for sample_id in sample_ids:
            if not gdd1.has_sample(sample_id):
                gdd2.add_geo_id(sample_id)
        
    dt2=DataCleaner.DataTable(probe_column, gene_column, collision, bad_data)
    dt2.getGEOData(gdd2)
        
    # now do things that buildCSVData does:
    # begin_copy_and_paste
    # whoops! added changes, no longer an exact copy! ha ha!
    dp = DataPackager.dataPackager(merge_cache=".")
    gnf = GMTParser.GMTParser(gnfile)
    dp.addGeneNetwork(gnf.getAllNetworks())
    dp.addSynonyms(synfile)
    #add data table
    dp.addDataTable(dt1)
    dp.addDataTable(dt2)
    

    # create subsets(classes)
    # this is where the edits are
    dp.createClassification(pheno1)
    for samp in gdd1.samples:
        dp.addToClassification(pheno1, dt1.dt_id, samp)
    dp.createClassification(pheno2)
    for samp in gdd2.samples:
        dp.addToClassification(pheno2, dt2.dt_id, samp)
    return dp
    # end_copy_and_base

def extractTSP( datapackage, config, tsp):
    output_object = {}
    output_object['type'] = 'tsp'
    max_scores = tsp.getMaxScores()
    row_key = config.getSetting("tsp","Row Key(genes/probes)")[0]
    #convert indices to genes/probes
    #Note: classification rule is, if gene 1 is more highly expressed than gene 2 then classify as phenotype 1 otherwise phenotype 2
    output_object['gene_pairs'] = []
    for g1_index, g2_index in max_scores:
        #print g1_index
        #print g2_index
        output_object['gene_pairs'].append( (datapackage.getGeneName(g1_index, row_key), datapackage.getGeneName(g2_index, row_key)) )
    return json.dumps(output_object)

def extractkTSP( datapackage, config, ktsp):
    output_object = {}
    output_object['type'] = 'ktsp'
    max_scores = ktsp.getMaxScores()
    row_key = config.getSetting("ktsp","Row Key(genes/probes)")[0]
    #convert indices to genes/probes
    #Note: classification rule is, if gene 1 is more highly expressed than gene 2 then classify as phenotype 1 otherwise phenotype 2
    output_object['gene_pairs'] = []
    for g1_index, g2_index in max_scores:
        output_object['gene_pairs'].append( (datapackage.getGeneName(g1_index, row_key), datapackage.getGeneName(g2_index, row_key)) )
    return json.dumps(output_object)
       

def extractTST( datapackage, config, tst):
    output_object = {}
    output_object['type'] = 'tst'
    ms = tst.getMaxScores()
    row_key = config.getSetting("tst","Row Key(genes/probes)")[0]
    output_object['genes'] = []
    for genes in ms:
        column = 0
        tab = ''
        gene_map = {}
        for i,gene in enumerate(genes):
            gene_name = datapackage.getGeneName(gene, row_key)
            gene_map['g' + str(i+1)] = gene_name
        output_object['genes'].append(gene_map)
    #NOTE: 'g1,g2,g3' = g1 <= g2 <= g3

    orders = ['g1,g2,g3', 'g1,g3,g2', 'g2,g1,g3', 'g2,g3,g1', 'g3,g1,g2', 'g3,g2,g1']
    output_object['tables'] = []
    ptable = tst.ptable
    #print ptable
    for triplet in ptable:
        #print triplet
        order_map = {}
        for o, order in enumerate(orders):
            order_map[order] = (triplet[0][o], triplet[1][o])
        output_object['tables'].append(order_map)
    return json.dumps(output_object) 

def trainDirac( datapackage, config ):
    min_net = config.getSetting("dirac","Minimum Network Size")[0]
    row_key = config.getSetting("dirac","Row Key(genes/probes)")[0]
    numTopNetworks = config.getSetting("dirac","Number of Top Networks")[0]
    data_vector, num_genes = datapackage.getDataVector(row_key)
    class_vector = datapackage.getClassVector()

    gene_net, gene_net_size = datapackage.getGeneNetVector(min_net)
    netMap = datapackage.gene_net_map
    d = dirac.Dirac(data_vector, num_genes,class_vector, gene_net, gene_net_size, numTopNetworks, netMap)
    d.train()
    return d

def trainTSP( datapackage, config):
    """
    Performs the training of TSP
    """
    filters = config.getSetting("tsp","filters")
    row_key = config.getSetting("tsp","Row Key(genes/probes)")[0]
     
    data_vector, num_genes = datapackage.getDataVector(row_key)
    class_vector = datapackage.getClassVector()
    vecFilter = tsp.IntVector()
    for val in filters:
        vecFilter.push_back(val)

    t = tsp.TSP(data_vector, num_genes, class_vector, vecFilter)
    t.train()
    return t

def trainTST(datapackage, config ):
    """
    Performs the training of tst
    """
    filters = config.getSetting("tst","filters")
    row_key = config.getSetting("tst","Row Key(genes/probes)")[0]
     
    data_vector, num_genes = datapackage.getDataVector(row_key)
    class_vector = datapackage.getClassVector()
    vecFilter = tst.IntVector()
    for val in filters:
        vecFilter.push_back(val)
    t = tst.TST(data_vector, num_genes, class_vector, vecFilter)    
    t.train()
    return t

def trainkTSP(datapackage, config ):
    """
    Performs the training of k-TSP
    """
    maxk = config.getSetting("ktsp","Maximum K value")[0]
    cross_remove = config.getSetting("ktsp","Remove for Cross Validation")[0]
    num_cross = config.getSetting("ktsp","Number of Cross Validation Runs")[0]
    row_key = config.getSetting("ktsp","Row Key(genes/probes)")[0]
    data_vector, num_genes = datapackage.getDataVector(row_key)
    filters = config.getSetting("ktsp","filters")
    class_vector = datapackage.getClassVector()
    vecFilter = tst.IntVector()
    for x in filters:
        if x < 2*maxk:
            raise Exception("Ktsp setting error.  The filters must be at least twice the Maximum K value")
        vecFilter.push_back(x)

    
    k = ktsp.KTSP( data_vector, num_genes, class_vector, vecFilter, maxk, cross_remove, num_cross)
    k.train()
    return k
    


def get_options():
    """
    sample call:   python aurea.py -anormal.csv -btumor.csv -ltsp -cconfig.xml
    """
    parser = OptionParser()
    parser.add_option("-a", "--table_1", dest="input_file_one",
                        help="csv file for class 1")
    parser.add_option("-b", "--table_2", dest="input_file_two",
                        help="csv file for class 2")

    parser_add_option("-p1", "--pheno1", dest="pheno1", 
                      help="phenotype name")

    # debugging use only, I think
    parser_add_options("-p2", "--pheno2", dest="pheno2", default=None,
                       help="second phenotype name")

    parser.add_option("-l", "--learner", dest="learner",
                        help="learner to train (tsp, tst, ktsp, dirac, adaptive)")
    parser.add_option("-c", "--config", dest="config_file",
                        help="xml file containing the learner settings")
    parser.add_option("-o", "--output", dest="output_file",
                        help="file in which to write output(defaults to std out)")
    
    (options, args) = parser.parse_args()
    return (options, args)
    
########################################################################

if __name__ == "__main__":
    (options, args)=get_options()
    print runAUREA(options)





    

