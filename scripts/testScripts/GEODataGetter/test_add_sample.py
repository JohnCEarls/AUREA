import unittest, sys, os
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from AUREA.packager.DataCleaner import DataTable
from AUREA.parser.GEODataGetter import GEODataGetter
from GEO.Sample import Sample
from warn import *

gdd=None
class TestAddSample(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_add_sample(self):
        geo_id='GSM254724'
        global gdd
        if not gdd:
            gdd=GEODataGetter(geo_id)
        gdd.add_geo_id(geo_id)
        matrix=gdd.matrix

        sample=Sample(geo_id).populate()
        (id_type, sample_data)=sample.expression_data(id_type='probe')
        si=gdd.sample_index[geo_id]
        for id,exp_val in sample_data.items():
            if id not in gdd.probe_index: continue # some probes are skipped
            gi=gdd.probe_index[id]
            self.assertEqual(matrix[gi][si], exp_val, 
                             msg="%s: [%s][%s]=%s, expected %s" % (id, gi,si, matrix[gi][si], exp_val))




suite = unittest.TestLoader().loadTestsFromTestCase(TestAddSample)
unittest.TextTestRunner(verbosity=2).run(suite)


        

