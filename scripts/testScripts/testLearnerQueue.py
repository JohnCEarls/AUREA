AUREA_dir = '/home/earls3/Price/AUREA'

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
    gene_network_file = AUREA_dir +"/workspace/data/c2.biocarta.v2.5.symbols.gmt"
    synonym_file = AUREA_dir + "/workspace/data/Homo_sapiens.gene_info.gz"
    
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

if __name__ == "__main__":
    dp = createDataPackage(AUREA_dir+"/workspace/data/GDS2545.soft.gz",  "normal prostate adjacent to tumor", "primary prostate tumor" )

    lq = adaptiveGetLearnerQueue(dp)
    for x in lq:
        print "."
    print "done"

