import unittest, sys, os

sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from warn import *
from AUREA.parser.GEODataGetter import GEODataGetter
from GEO.Series import Series

gdd=None

class TestGDD(unittest.TestCase):
    
    def setUp(self):
#        os.environ['DEBUG']=str(True)
        pass
       
    def test_add_series(self):
        geo_id='GSE10072'
        global gdd
        if not gdd:
            gdd=GEODataGetter(geo_id)
        gdd.add_geo_id(geo_id)
        matrix=gdd.matrix

        series=Series(geo_id).populate()
        self.assertEqual(series.title, 'Gene expression signature of cigarette smoking and its role in lung adenocarcinoma development and survival') # just to ensure that it's in the db

        for sample_id in series.sample_ids:
            sample=Sample(sample_id)
            (id_type, sample_data)=sample.expression_data(id_type='probe')
            si=gdd.sample_index[geo_id]
            for id,exp_val in sample_data.items():
                gi=gdd.probe_index[id]
                self.assertEqual(matrix[gi][si], exp_val, msg="%s: [%s][%s]=%s" % (id, gi,si, exp_val))


        


        # check to see that all genes present; also, indexes
        # check to see that all probes present; also, indexes
        # check to see that len(samples)==1




suite = unittest.TestLoader().loadTestsFromTestCase(TestGDD)
unittest.TextTestRunner(verbosity=2).run(suite)


        

