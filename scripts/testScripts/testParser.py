from AUREA.parser.SOFTParser import SOFTParser

sp = SOFTParser('/home/earls3/Price/AUREAPackage/src/AUREA/data/GDS2545.soft.gz')
sp.printTable()
for e in sp.getEntities():
    print e.prettyPrint()
