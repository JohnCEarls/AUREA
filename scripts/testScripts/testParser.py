from AHREA.parser.SOFTParser import SOFTParser

sp = SOFTParser('/home/earls3/Price/AHREAPackage/src/AHREA/data/GDS2545.soft.gz')
sp.printTable()
for e in sp.getEntities():
    print e.prettyPrint()
