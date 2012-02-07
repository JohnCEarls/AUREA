import unittest, sys, os

sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'build', 'lib.linux-x86_64-2.7'))
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'scripts', 'testScripts'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))

from warn import *
import aurea_v

class TestAurea(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_getPhenoData(self):
        (options, args)=aurea_v.getOptions()
        options.pheno1='normal'
        dp=aurea_v.getPhenoData(options)



suite = unittest.TestLoader().loadTestsFromTestCase(TestAurea)
unittest.TextTestRunner(verbosity=2).run(suite)
