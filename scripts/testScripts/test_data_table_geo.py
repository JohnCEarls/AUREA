import unittest, sys, os

sys.path.append(os.environ['AUREA_SRC'])
from packager import DataCleaner

class TestDataTableGeo(unittest.TestCase):
    def setUp(self):
        self.data_table=DataCleaner.DataTable()
        self.assertIsInstance(self.data_table, DataCleaner.DataTable)

    def test_add_sample(self):
        my dt=self.data_table
        dt.add_sample(GEO.Sample('GSM4230', 'gene'))
        self.assertEqual(dt.getData('GSM4230', 'TIE1'), 149.725)
        self.assertEqual(dt.getData('GSM4230', 'RABEPK'), 112.463)

suite = unittest.TestLoader().loadTestsFromTestCase(TestDataTableGeo)
unittest.TextTestRunner(verbosity=2).run(suite)
