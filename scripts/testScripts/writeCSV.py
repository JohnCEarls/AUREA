from AUREA.parser.SOFTParser import SOFTParser
from AUREA.packager.DataCleaner import DataTable
from AUREA.packager.DataPackager import dataPackager
if __name__ == "__main__":
    path = "/home/earls3/Price/AUREA/workspace/data/"
    f1 = "GDS2545.soft.gz"
    sp = SOFTParser(path + f1)
    t1s = []
    t2s = []
    for x in sp.getSubsets():
        if x.attributes['subset_description'][0] == 'normal prostate tissue':
            t1s = sp.getSubsetSamples(x)
        if x.attributes['subset_description'][0] == 'primary prostate tumor':
            t2s = sp.getSubsetSamples(x)
            
    dt = DataTable()
    dt.getSOFTData(sp)
    dp = dataPackager(merge_cache=".")
    dp.addDataTable(dt)
    dp.createClassification("Normal")
    dp.createClassification("ignore")
    for samp in t1s:
        dp.addToClassification("Normal", dt.dt_id, samp)
    dp.writeToCSV("normal.csv", key='probe')
    dp.clearClassification()
    dp.createClassification("Tumor")
    dp.createClassification("ignore")
    for samp in t2s:
        dp.addToClassification("Tumor", dt.dt_id, samp)
    dp.writeToCSV("tumor.csv", key='probe')
 

