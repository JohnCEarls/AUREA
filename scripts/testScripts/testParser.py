from parser.SOFTParser import SOFTParser

sp = SOFTParser('downloaded/GDS463.soft.gz')
for e in sp.getEntities():
    print e.prettyPrint()
