from parser import SOFTParser, GMTParser
from packager import DataCleaner
from packager import DataPackager
"""
Some cheap scripts to facilitate testing the data building portion
of AUREA
"""


if __name__ == "__main__":
    print "starting parser"
    sp = SOFTParser.SOFTParser("data/GDS2545.soft.gz")
    sp2 = SOFTParser.SOFTParser("data/GDS1059.soft.gz")
    sp3 = SOFTParser.SOFTParser("data/GDS3329.soft.gz")
    gnfile = "data/c2.biocarta.v2.5.symbols.gmt"
    print "creating Table"
    dt1 = DataCleaner.DataTable()
    print "importing parser"
    dt1.getSOFTData(sp)
    print "gene parser"
    dt2 = DataCleaner.DataTable()
    print "importing parser"
    dt2.getSOFTData(sp2)
    dt3 = DataCleaner.DataTable()
    print "importing parser"
    dt3.getSOFTData(sp3)
    gnf = GMTParser.GMTParser(gnfile)
    print "data packager"
    dp = DataPackager.dataPackager()
    dp.addGeneNetwork(gnf.getAllNetworks())
    print "adding data table 1"
    dp.addDataTable(dt1)
    print "adding data table 2"
    dp.addDataTable(dt2)
    dp.addDataTable(dt3)
    dp.createClassification("first")
    dp.createClassification("post")
    for val in dt1.getSamples()[:len(dt1.getSamples())/2]:
        dp.addToClassification("first", dt1.dt_id, val)
    for val in dt2.getSamples()[len(dt2.getSamples())/2:]:
        dp.addToClassification("post", dt2.dt_id, val)
    for val in dt3.getSamples()[len(dt3.getSamples())/2:]:
        dp.addToClassification("post", dt3.dt_id, val)
  
    pdv, numProbes = dp.getDataVector('probe') 
    print [x for x in pdv]
    gdv, numGenes = dp.getDataVector('gene')

    if numProbes > 0:
        dp.writeToCSV("data/testPackagerProbes1.csv", "probe")
    else:
        print "No matching probes"
        
    if numGenes > 0:
        dp.writeToCSV("data/testPackagerGenes.csv", "gene")
