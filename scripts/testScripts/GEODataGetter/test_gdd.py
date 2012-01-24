import unittest, sys, os

sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from warn import *
from GEO.Sample import Sample
from GEO.Series import Series
from GEO.Dataset import Dataset
from AUREA.parser.GEODataGetter import GEODataGetter

class TestGDD(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_add_sample(self):
        geo_id='GSM00001'
        gdd=GEODataGetter(geo_id)
        gdd.add_geo_id(geo_id)
        matrix=gdd.matrix

        sample=Sample(geo_id)
        (id_type, sample_data)=sample.expression_data(id_type='probe')
        si=gdd.sample_index[geo_id]
        for id,exp_val in sample_data.items():
            gi=gdd.probe_index[id]
            self.assertEqual(matrix[gi][si], exp_val, msg="%s: [%s][%s]=%s" % (id, gi,si, exp_val))

    def test_add_series(self):
        geo_id='GSE001'
        gdd=GEODataGetter(geo_id)
        series=Series(geo_id)
        gdd.add_geo(series)
        


    def test_add_dataset(self):
        pass





suite = unittest.TestLoader().loadTestsFromTestCase(TestGDD)
unittest.TextTestRunner(verbosity=2).run(suite)


        

