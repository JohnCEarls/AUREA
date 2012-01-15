import unittest, sys, os
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from GEO.Sample import Sample
from AUREA.parser.GEODataGetter import GEODataGetter

from warn import *

class TestBabel(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_babel(self):
        gdg=GEODataGetter()
        pairs=[
            ['DDR1', '1007_s_at'],
            ['RFC2', '1053_at'],
            ['HSPA6', '117_at'],
            ['PAX8', '121_at'],
            ['GUCA1A', '1255_g_at'],
            ['UBA7', '1294_at'],
            ['THRA', '1316_at'],
            ['PTPN21', '1320_at'],
            ['CCL5', '1405_i_at'],
            ['CYP2E1', '1431_at'],
            ['EPHB3', '1438_at'],
            ['ESRRA', '1487_at'],
            ['CYP2A6', '1494_f_at'],
            ['GAS6', '1598_g_at'],
            ['MMP14', '160020_at'],
            ['TRADD', '1729_at'],
            ]
        
        for pair in pairs:
            self.assertEqual(gdg.probe2gene(pair[1]), pair[0])
            self.assertIn(pair[1], gdg.gene2probes(pair[0]))



suite = unittest.TestLoader().loadTestsFromTestCase(TestBabel)
unittest.TextTestRunner(verbosity=2).run(suite)


        

