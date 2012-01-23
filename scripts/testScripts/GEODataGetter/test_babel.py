import unittest, sys, os
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from GEO.Sample import Sample
from AUREA.parser.GEODataGetter import GEODataGetter
from AUREA.parser.affyprobe2genesymbol import AffyProbe2GeneSymbol
from warn import *

gdd=None

class TestBabel(unittest.TestCase):
    def setUp(self):
        global gdd
        if not gdd:
            warn("creating gdd")
            gdd=GEODataGetter('no_name')
        
    def test_babel(self):
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
            self.assertEqual(gdd.probe2gene(pair[1]), pair[0])
            self.assertIn(pair[1], gdd.gene2probes(pair[0]))


    def test_all(self):
        p2g=gdd.p2g
        g2p=gdd.g2p
        self.assertIsInstance(p2g, dict)
        self.assertEqual(len(p2g), 156598)
        self.assertEqual(p2g['1598_g_at'], 'GAS6')

        self.assertIn('GAS6', g2p)
        self.assertIsInstance(g2p['GAS6'], list)
        self.assertIn('1598_g_at', g2p['GAS6'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestBabel)
unittest.TextTestRunner(verbosity=2).run(suite)


        

