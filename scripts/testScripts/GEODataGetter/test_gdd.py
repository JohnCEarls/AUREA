import unittest, sys, os

sys.path.append(os.environ['AUREA_SRC'])
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from warn import *
from parser.GEODataGetter import GEODataGetter

class TestGDD(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_add_sample(self):
        gdd=GEODataGetter()
        geo_id='GSM00001'
        gdd.add_geo_id(geo_id)
        table=gdd.table()

    def _test_add_sample(self, gdd, test_ids):
        sample=Sample(geo_id).populate()
        data=sample.expression_data(id_type) # data ignored (so far)
        dt.add_sample(sample, id_type)
        warn("%s: %d x %d(%d) (n_samples, n_genes, n_probes)" % 
             (geo_id, len(dt.getSamples()), dt.getNumGenes(), dt.getNumProbes()))
#        warn("%s: dt.data_table is\n%s" %(geo_id, dt.data_table))

        # check to see that all genes present; also, indexes
        # check to see that all probes present; also, indexes
        # check to see that len(samples)==1




suite = unittest.TestLoader().loadTestsFromTestCase(TestGDD)
unittest.TextTestRunner(verbosity=2).run(suite)


        

