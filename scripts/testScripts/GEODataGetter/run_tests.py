import unittest, sys, os

sys.path.append(os.path.join(os.environ['AUREA_HOME'], 'src'))
sys.path.append(os.path.join(os.environ['TRENDS_HOME'], 'pylib'))
import GEO

suite=unittest.TestLoader().discover('.',pattern='test*.py')
unittest.TextTestRunner(verbosity=2).run(suite)
