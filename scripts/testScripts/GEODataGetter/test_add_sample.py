import unittest, sys, os
sys.path.append(os.environ['AUREA_SRC'])
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from packager.DataCleaner import DataTable
from GEO.Sample import Sample
from warn import *

class TestAddSample(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_add_sample(self):
        pass



suite = unittest.TestLoader().loadTestsFromTestCase(TestAddSample)
unittest.TextTestRunner(verbosity=2).run(suite)


        

