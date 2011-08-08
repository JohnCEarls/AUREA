"""
Script from cluster
"""
import time

def paperTest(dataPackage):
    print "tsp, tst, kTSP, dirac, Adaptive" 
    print testTSP(dataPackage, [100,100], 10),
    print ", ",
    print testTST(dataPackage, [10,10,10], 10),
    print ", ",
    print testkTSP(dataPackage, [100,100], 10, 10),
    print ", ",
    print testDirac(dataPackage, 1, 10),
    print ", ",
    print testAdaptive(dataPackage, 3600, 1.0, 10)

def createDataPackage(dataFile, subset1, subset2 ):
    """
    Builds a DataPackager
    """
    from AUREA.packager.DataPackager import dataPackager
    from AUREA.parser.SOFTParser import SOFTParser
    from AUREA.packager.DataCleaner import DataTable
    from AUREA.parser.GMTParser import GMTParser
    #get soft file
    sp = SOFTParser( dataFile )
    ss_list = [None, None]
    for ss in sp.getSubsets():
        if subset1 in ss.attributes['subset_description']:
            ss_list[0] = ss
        if subset2 in ss.attributes['subset_description']:
            ss_list[1] = ss
    subsetSamples1 = sp.getSubsetSamples( ss_list[0] )
    subsetSamples2 = sp.getSubsetSamples( ss_list[1] )
    #make a data table
    dt = DataTable()
    dt.getSOFTData( sp )
    #add stuff to build networks
    gene_network_file = "/home/earls3/lib/AUREA/workspace/data/c2.biocarta.v2.5.symbols.gmt"
    synonym_file = "/home/earls3/lib/AUREA/workspace/data/Homo_sapiens.gene_info.gz"
    
    #set up classes
    dp = dataPackager()
    dp.addSynonyms(synonym_file)
    gn = GMTParser(gene_network_file) 
    dp.addGeneNetwork(gn.getAllNetworks())
    dp.addDataTable(dt)
    dp.createClassification(subset1)
    dp.createClassification(subset2)
    for sample in subsetSamples1:
        dp.addToClassification( subset1, dt.dt_id, sample )
    for sample in subsetSamples2:
        dp.addToClassification( subset2, dt.dt_id, sample )
    return dp
    
    
def adaptiveGetLearnerQueue(dataPackage):
    import AUREA.heuristic.LearnerQueue as lq
    #build training package
    
    learner_queue = lq.LearnerQueue(dataPackage, scale=[5741.666666666449, 35880937.02218559, 41600.0, 43098104.318478584])
    learner_queue.genDirac((3,15,3),(1,9,2))
    learner_queue.genKTSP((10, 21, 2), (1,2,1), (0,1,1),(50,1000,10), (50,1000,10))
    learner_queue.genTSP((10, 1000, 10), (10, 1000, 10))
    learner_queue.genTST((10, 100, 25), (10, 200, 25), (10,100,25))
    #print "learner queue built"
    return learner_queue  


def testTSP( dataPackage, filters, kfold):
    """
    Runs cross validation on TSP.
    """
    import AUREA.learner.tsp as tsp
    data, numProbes = dataPackage.getDataVector( 'probe' ) 
    classVector = dataPackage.getClassVector()
    filterVec = tsp.IntVector(filters)
    tsp_learner = tsp.TSP( data, numProbes , classVector, filterVec )
    return tsp_learner.crossValidate(kfold)

def testTST(dataPackage, filters, kfold):
    import AUREA.learner.tst as tst 
    data, numProbes = dataPackage.getDataVector( 'probe' ) 
    classVector = dataPackage.getClassVector()
    filterVec = tst.IntVector(filters)
    tst_learner = tst.TST( data, numProbes , classVector, filterVec )
    return tst_learner.crossValidate(kfold)
 
def testkTSP(dataPackage, filters, maxk, kfold):
    import AUREA.learner.ktsp as ktsp
    data, numProbes = dataPackage.getDataVector( 'probe' ) 
    classVector = dataPackage.getClassVector()
    filterVec = ktsp.IntVector(filters)
    ktsp_learner = ktsp.KTSP( data, numProbes, classVector, filterVec, maxk, 0, 1)
    return ktsp_learner.crossValidate(kfold)
  
    
def testDirac(dataPackage, numNets, kfold):
    import AUREA.learner.dirac as dirac
    data, numGenes = dataPackage.getDataVector( 'gene' )
    classVector = dataPackage.getClassVector()
    geneNet, geneNetSize = dataPackage.getGeneNetVector(1)
    netMap = dataPackage.gene_net_map
    dirac_learner = dirac.Dirac( data, numGenes, classVector, geneNet, geneNetSize, numNets, netMap)
    return dirac_learner.crossValidate( kfold )

def testAdaptive(dataPackage, time, target_acc, kfold):
    from copy import deepcopy
    from AUREA.heuristic.Adaptive import Adaptive
    #partition the samples
    lq = adaptiveGetLearnerQueue(dataPackage)
    adaptive = Adaptive(lq)
    return adaptive.crossValidate(target_acc,time, kfold)


if __name__ == "__main__":
    import inspect
    import sys
    folder = "/home/earls3/Archive/AHREA/downloaded/"
    data_file = ["GDS3329.soft.gz",  "GDS2545.soft.gz","GDS2545.soft.gz", "GDS843.soft.gz", "GDS1059.soft.gz","GDS1209.soft.gz", "GDS1210.soft.gz", "GDS1269.soft.gz", "GDS1330.soft.gz", "GDS1330.soft.gz", "GDS1330.soft.gz"]

    s1 = ['peripheral blood', "normal prostate adjacent to tumor","primary prostate tumor", "clinical outcome - alive", "complete remission", "normal", "normal","non-smoker control", "normal", "normal", "ulcerative colitis" ]
    s2 = ['bone marrow',"primary prostate tumor","normal prostate tissue", "clinical outcome - dead", "relapse", "sarcoma", "cancer", "smoker", "Crohn disease","ulcerative colitis", "Crohn disease" ]
    i = int(sys.argv[1])
    print data_file[i]
    #print "batch = " + str(sys.argv[2])
    dp = createDataPackage(folder + data_file[i], s1[i], s2[i]) 
    paperTest( dp )
   
