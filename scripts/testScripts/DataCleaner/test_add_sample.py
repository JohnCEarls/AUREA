import unittest, sys, os, yaml
sys.path.append(os.environ['AUREA_SRC'])
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from packager.DataCleaner import DataTable
from GEO.Sample import Sample
from warn import *

class TestAddSample(unittest.TestCase):
    
    def setUp(self):
        pass


    def test_GSM00001(self):
        id_list=['1007_s_at','1053_at','117_at','121_at','1255_g_at','1294_at','1316_at','1320_at',
                 '1405_i_at','1431_at','1438_at','1487_at','1494_f_at','1598_g_at','160020_at','1729_at']
        self._test_add_sample('GSM00001',  'probe', id_list)

    def test_GSM15718(self):
        id_list=['200003_s_at', '1438_at', '200707_at', '200773_x_at', '200981_x_at', '91682_at']
        self._test_add_sample('GSM15718',  'probe', id_list)
        
    def test_add_2(self):
        

    def _test_add_sample(self, geo_id, id_type, id_list):
        dt=DataTable()
        sample=Sample(geo_id).populate()
        data=sample.expression_data(id_type) # data ignored (so far)
        dt.add_sample(sample, id_type)
        warn("%s: %d x %d(%d) (n_samples, n_genes, n_probes)" % 
             (geo_id, len(dt.getSamples()), dt.getNumGenes(), dt.getNumProbes()))
#        warn("%s: dt.data_table is\n%s" %(geo_id, dt.data_table))

        # shouldn't be any gene data:
        # fixme: this will break when we call with genes
        self.assertEqual(dt.genes, None)
        if dt.gene_index:
            self.assertEqual(len(dt.gene_index), 0)

        # check probe data:
        self.assertEqual(len(dt.probe_index), len(sample.data[id_type]))
        for probe_id in id_list:
            self.assertEqual(dt.getData(geo_id, probe_name=probe_id), 
                             sample.expression_data(id_type)[probe_id])
        

        # check dt.sample stuff
        self.assertEqual(len(dt.samples),1)
        self.assertEqual(dt.samples[0], geo_id)
        self.assertEqual(dt.sample_index, {geo_id:0})
        if hasattr(sample, 'description'):
            self.assertEqual(dt.getSampleDescription(geo_id), sample.description)
        self.assertIn(geo_id, dt.getSamples())




suite = unittest.TestLoader().loadTestsFromTestCase(TestAddSample)
unittest.TextTestRunner(verbosity=2).run(suite)


        

