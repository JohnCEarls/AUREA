import unittest, sys, os
sys.path.append(os.environ['AUREA_SRC'])
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from packager.DataCleaner import DataTable
from GEO.Sample import Sample
from warn import *

class TestAddToDataTable(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_add_to_data_table(self):
        pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestAddToDataTable)
unittest.TextTestRunner(verbosity=2).run(suite)


        

