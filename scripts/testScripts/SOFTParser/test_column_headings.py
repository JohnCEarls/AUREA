import unittest, sys, os, yaml

sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from warn import *
from AUREA.parser.SOFTParser import SOFTParser
from GEO.Dataset import Dataset

class TestSOFTParser(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_column_heading_info(self):
        geo_id='GDS1022'
        dataset=Dataset(geo_id)
        sp = SOFTParser(dataset.soft_file())
        print yaml.dump(sp.column_heading_info)

        



suite = unittest.TestLoader().loadTestsFromTestCase(TestSOFTParser)
unittest.TextTestRunner(verbosity=2).run(suite)


        

