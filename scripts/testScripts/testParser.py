import sys, os
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
from AUREA.parser.SOFTParser import SOFTParser

filename='/home/ISB/vcassen/l/trends/data/GEO/datasets/GDS2545.soft'
#filename='/home/earls3/Price/AUREAPackage/src/AUREA/data/GDS2545.soft.gz'
sp = SOFTParser(filename)
#sp.printTable()
for e in sp.getEntities():
    print e.prettyPrint()
