from AUREA.learner import ktsp, tst, dirac, tsp
from AUREA.parser import SOFTParser, GMTParser
from AUREA.packager import DataCleaner, DataPackager
from AUREA.adaptive import ResourceEstimate
from AUREA.adaptive import LearnerQueue
import random
import string
def getDataPackage():
    dd = "/home/earls3/Price/AUREAPackage/src/AUREA/data/"
    softfile = dd+"GDS2545.soft.gz"


    gnfile  = dd+"c2.biocarta.v2.5.symbols.gmt"
    synfile = dd+"Homo_sapiens.gene_info.gz"
    gnf = GMTParser.GMTParser(gnfile)

    sp = SOFTParser.SOFTParser(softfile)

    normal = []
    tumor = []
    for line in sp.column_heading_info[0]:
        if string.find(line[1], 'normal prostate tissue free') > 0:
            normal.append(line[0].strip())
        elif string.find(line[1], 'tumor') > 0:
            tumor.append(line[0].strip())

    dt = DataCleaner.DataTable()
    dt.getSOFTData(sp)
    dp = DataPackager.dataPackager()
    dp.addGeneNetwork(gnf.getAllNetworks())
    dp.addDataTable(dt)
    dp.addSynonyms(synfile)
    dp.createClassification("Tumor")
    dp.createClassification("Normal")
    for samp in tumor:
        dp.addToClassification("Tumor", dt.dt_id, samp)


    for samp in normal[:-1]:
        dp.addToClassification("Normal", dt.dt_id, samp)
    dp.setUnclassified(dt.dt_id, normal[-1])
    return dp

from AUREA.learner import ktsp, tst, dirac, tsp
dp = getDataPackage()
min_net = 1

row_key = 'gene'
data_vector, num_genes = dp.getDataVector(row_key)
class_vector = dp.getClassVector()
gene_net, gene_net_size = dp.getGeneNetVector(min_net)
print "Making Dirac"
d =dirac.Dirac(data_vector, num_genes,class_vector, gene_net, gene_net_size)
print "dirac is made"
d.train()
d.crossValidate()
print "done crossV"
udv =dp.getUnclassifiedDataVector('gene')
print "in addUnclassified"
d.addUnclassified(dp.getUnclassifiedDataVector('gene'))
print "in classify()"
d.classify()





