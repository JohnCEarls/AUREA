import unittest, sys, os, bson

sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from warn import *
from AUREA.parser.GEODataGetter import GEODataGetter
import GEO

gdd=GEODataGetter(__file__)


class TestGDD(unittest.TestCase):
    
    def setUp(self):
        global gdd
        gdd.clear()

    def _test_GSE001(self):
        # set the data_dir to use fixtures:
        GEO.GEOBase.GEOBase._data_dir=os.path.join(os.environ['TRENDS_HOME'], 't', 'fixtures', 'data', 'GEO')
        self.assertEqual(GEO.Sample.Sample.data_dir(), GEO.GEOBase.GEOBase.data_dir())

        self._test_add_series('GSE001')
        gdd.writeCSV(os.path.join(os.path.dirname(__file__), 'GSE001.csv'))
#        gdd.write_gene_index(os.path.join(os.path.dirname(__file__), 'GSE001.gene_index'))

        # test specifics:
        self.assertEqual(gdd.n_genes(), 0)
        self.assertEqual(gdd.n_probes(), 16)
        self.assertEqual(gdd.n_samples, 10)

        # UBA7 removed from GSM0003
        matrix=gdd.matrix
#        self.assertEqual(matrix[gdd.gene_index['UBA7']][gdd.sample_index['GSM0003']], 0)
        self.assertEqual(matrix[gdd.probe_index['1294_at']][gdd.sample_index['GSM0003']], 0)

        # test ADD[123] from GSM00004:

    def _test_GSE10072(self):
        GEO.GEOBase.GEOBase._data_dir=os.path.join(os.environ['TRENDS_HOME'], 'data', 'GEO')
        GEO.GEOBase.data_dir=os.path.join(os.environ['TRENDS_HOME'], 'data', 'GEO')
        self._test_add_series('GSE10072')

    def test_GSE10072_masked(self):
        GEO.GEOBase.GEOBase._data_dir=os.path.join(os.environ['TRENDS_HOME'], 'data', 'GEO')
        GEO.GEOBase.data_dir=os.path.join(os.environ['TRENDS_HOME'], 'data', 'GEO')

        gdd.use_mask=True
        probes=['1053_at','117_at','121_at','1255_g_at','1316_at','1320_at','1405_i_at',
                '1431_at','1438_at','1487_at','1494_f_at','1598_g_at','160020_at','1729_at']
        for probe in probes: gdd.mask[probe]=probe

        self._test_add_series('GSE10072')
        self.assertEqual(len(gdd.probes()), len(probes))

        series=GEO.Series.Series('GSE10072').populate()
        self.assertEqual(len(series.samples()), len(gdd.samples))

    def _test_add_series(self, geo_id):
        gdd.add_geo_id(geo_id)
        matrix=gdd.matrix

        series=GEO.Series.Series(geo_id).populate()
        self.assertIsInstance(series._id, bson.objectid.ObjectId)

        warn("checking sample_index for all samples")
        for sample_id in series.sample_id:
            self.assertIn(sample_id, gdd.sample_index)

        warn("checking samples...")
        for sample_id in series.sample_id:
            sample=GEO.Sample.Sample(sample_id)
            (id_type, sample_data)=sample.expression_data('probe')
            i_sample=gdd.sample_index[sample_id]

            # check every probe in every sample...
            for id,exp_val in sample_data.items():
                try: gi=gdd.probe_index[id]
                except KeyError: continue # happens during masked test
                    
                self.assertAlmostEqual(matrix[gi][i_sample], exp_val, delta=0.001,
                                   msg="%s: [%s][%s]=%s, not %s (%s)" % (id, gi, i_sample, matrix[gi][i_sample], exp_val, sample_id))


        # check to see that all genes present; also, indexes
        # check to see that all probes present; also, indexes
        # check to see that len(samples)==1


    def verify_indexes(self):
        # make sure that all gene and probe indexes match
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestGDD)
unittest.TextTestRunner(verbosity=2).run(suite)


        

