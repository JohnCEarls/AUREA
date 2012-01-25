import unittest, sys, os
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

import GEO
from AUREA.packager.DataCleaner import DataTable
from AUREA.parser.GEODataGetter import GEODataGetter
from GEO.Sample import Sample
from warn import *


gdd=None
class TestAddSample(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_GSM00001(self):
        GEO.GEOBase.data_dir=os.path.join(os.environ['TRENDS_HOME'], 't', 'fixtures', 'data', 'GEO')
        self._test_add_sample('GSM00001')
        gdd.write_gene_index(os.path.join(os.path.dirname(__file__), 'GSM00001.gene_index'))
        gdd.write_probe_index(os.path.join(os.path.dirname(__file__), 'GSM00001.probe_index'))
        gdd.write_sample_index(os.path.join(os.path.dirname(__file__), 'GSM00001.sample_index'))

    def _test_GSM254724(self):
        self._test_add_sample('GSM254724')

        
    def _test_add_sample(self, geo_id):
        global gdd
        if not gdd:
            gdd=GEODataGetter(geo_id)
        gdd.add_geo_id(geo_id, 'probe')
        matrix=gdd.matrix

        sample=Sample(geo_id).populate()
        (id_type, sample_data)=sample.expression_data('probe')
        si=gdd.sample_index[geo_id]
        for id,exp_val in sample_data.items():
            if id not in gdd.probe_index: continue # some probes are skipped
            gi=gdd.probe_index[id]
            self.assertAlmostEqual(matrix[gi][si], exp_val, delta=0.001,
                             msg="%s: [%s][%s]=%s, expected %s" % (id, gi,si, matrix[gi][si], exp_val))




suite = unittest.TestLoader().loadTestsFromTestCase(TestAddSample)
unittest.TextTestRunner(verbosity=2).run(suite)


        

