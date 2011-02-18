#!/usr/bin/python
"""
wilcoxon = open("test.txt");
w = []
for line in wilcoxon.readlines():
    gene, score = line.split(',')
    gene = gene.strip()
    score = score.strip()
    w.append((int(gene), float(score)))

"""



softfile = "data/GDS2545.soft.gz"
#softfile2 = "data/GDS3289.soft.gz"
gnfile = "data/c2.biocarta.v2.5.symbols.gmt"
synfile = "data/Homo_sapiens.gene_info.gz"
from learner import ktsp, tst, dirac, tsp
from parser import SOFTParser, GMTParser
from packager import DataCleaner, DataPackager
import string

print "SOFTParser"
sp = SOFTParser.SOFTParser(softfile)

normal = []
tumor = []
for line in sp.column_heading_info[0]:
    if string.find(line[1], 'normal prostate tissue free') > 0:
        normal.append(line[0].strip())
    elif string.find(line[1], 'tumor') > 0:
        tumor.append(line[0].strip())
print "Data Cleaner"
dt = DataCleaner.DataTable()
dt.getSOFTData(sp)

#print "SOFTParser2"
#sp2 = SOFTParser.SOFTParser(softfile2)
"""
for line in sp2.column_heading_info[0]:
    print line[0]
"""
#tumor = []
#for line in sp2.column_heading_info[0][2:]:
#    tumor.append(line[0].strip())
print "Data Cleaner"
#dt2 = DataCleaner.DataTable()
#dt2.getSOFTData(sp2)
#dt2.writeAsCSV("mytest.csv")

print "Gene Network Parser"
gnf = GMTParser.GMTParser(gnfile)

print "Data Packager"
dp = DataPackager.dataPackager()
dp.addGeneNetwork(gnf.getAllNetworks())
dp.addDataTable(dt)
#dp.addDataTable(dt2)
dp.addSynonyms(synfile)
print "Adding single class"
dp.createClassification("Tumor")
dp.createClassification("Normal")
for samp in tumor:
    dp.addToClassification("Tumor", dt.dt_id, samp)


for samp in normal:
    dp.addToClassification("Normal", dt.dt_id, samp)



print "classes added"
print "Getting Vectors"
cv = dp.getClassVector()
dv = dp.getDataVector("gene")
gn = dp.getGeneNetVector()
nvec = tsp.IntVector()
nvec.push_back(10)
nvec.push_back(10)
print "Dirac"
d = dirac.Dirac( dv[0], dv[1], cv,gn[0],gn[1] )
print d.crossValidate()
print "TSP"
t = tsp.TSP( dv[0], dv[1], cv, nvec)
print t.crossValidate()
nvec.push_back(10)
print "TST"
tt = tst.TST( dv[0], dv[1], cv, nvec)
print tt.crossValidate()
nvec = tsp.IntVector()
nvec.push_back(100)
nvec.push_back(10)
print "KTSP"
k = ktsp.KTSP( dv[0], dv[1], cv, nvec, 10, 0, 1)
print k.crossValidate()
exit()
udv = dp.getUnclassifiedDataVector("gene")
d.addUnclassified(udv)

print d.classify(10)
print 
#dp.writeToCSV('data/test.csv', 'gene')
exit()
nvec = tsp.IntVector()
classes = len(dv[0])/dv[1]
max = 0.0
for gene, value in w:
    if value < max:
        break
    prevTable = None
    print dp.getGeneName(gene),
    for classification, samples in dp.classifications:
        for table, sample in samples:
            if prevTable != table:
                t_obj = dp.getTable(table)
                prevTable = table
            print t_obj.getData(sample, dp.getGeneName(gene), None),
            print '\t',
    print
            
    max = value
"""
nvec.push_back(10)
nvec.push_back(10)
print "training tst"

nvec.push_back(10)
tt = tst.TST(dv[0], dv[1], cv, nvec)
tt.train()
print "TST complete"
"""
"""
def fac( x):
    if x == 0:
        return 1
    else:
        return x * fac(x-1)
print sum([ pow(2,(x*2)) for x in gn[1]])
"""
"""
print "Starting Dirac"
d1 = dirac.Dirac(dv[0],dv[1],cv, gn[0], gn[1])
prev = -1
for i in test:
    if i != prev:
        print dp.getGeneNetName(i)
        prev = i
print "Training Dirac"
d1.train()
gns = d1.getRankDifference()

rms = d1.getRankTemplates()
s = d1.getNetworkRankStart(2)
e = s+d1.getNetworkRankSize(2)
print rms[0][s:e]
print rms[0][s:e] 
for i in xrange(0,30):
    print dp.getGeneNetName(gns[i][1]),
    print gns[i][0],
    print gns[i][2]
#print d1.testAll()

#quit()
rms = d1.getRankMatchingScores()
#print rms
#quit()
print "training tsp"
nvec = tsp.IntVector()
nvec.push_back(10)
nvec.push_back(10)
t = tsp.TSP(dv[0], dv[1], cv, nvec)
t.train()
print "training tst"

nvec.push_back(10)
tt = tst.TST(dv[0], dv[1], cv, nvec)
tt.train()
"""
"""
print "training k-tsp"
maxK = 10
n = 0
m = 1 
topKPairs = ktsp.IntVector()
print "TSP"
kt = ktsp.KTSP(dv[0], dv[1],cv, maxK, n, m)
kt.train()
print "done"
"""

"""
dirac_count = 0
tsp_count = 0
tst_count = 0
ktsp_count = 0
testsamp = []
for x in tumor[-5:]:
    if x in dp.data_tables[-1].sample_index:
        testsamp.append(x)
numtumors =  len(testsamp)
for x in normal[-5:]:
    if x in dp.data_tables[-1].sample_index:
        testsamp.append(x)
#print testsamp
unclassified = None
prev = None

def compareVec(v1, v2):
    if v1 == None:
        return
    for i in xrange(len(v1)):
        if v1[i] == v2[i]:
            print "rutro"
count = 0
oldsamp = None
for samp in testsamp:
    print "classifying " + str(count)
    count +=1
    print "Dirac"
        
    dp.setUnclassified(dt.dt_id, samp)
    unclassified = dp.getUnclassifiedDataVector()
    
    d1.addUnclassified(unclassified)
    dclass = d1.classify(5)
    print dclass
    if not dclass[0][0] is not None:
        print "Tie"
    else:
        if count <= numtumors and dclass[0][0] == 0:
            dirac_count += 1
        elif count > numtumors and dclass[0][0] == 1:
            dirac_count += 1
        else:
            print "count = ",
            print count
            print "numtumors = ",
            print numtumors

    t.addUnclassified(unclassified) 
    tspclass = t.classify()
    if count <= numtumors and tspclass == 0:
            tsp_count += 1

    tsp_count += tspclass
    tt.addUnclassified(unclassified)
    tstclass =  tt.classify()
    if count <= numtumors and tstclass == 0:
            tst_count += 1

    tst_count += tstclass
    kt.addUnclassified(unclassified)
    ktspclass = kt.classify()
    if count <= numtumors and ktspclass == 0:
            ktsp_count += 1

    ktsp_count += ktspclass
print "numclassified"
print count
print "dirac count"
print dirac_count
print "tsp_count"
print tsp_count
print "tst_count"
print tst_count
print "ktsp_count"
print ktsp_count
"""
