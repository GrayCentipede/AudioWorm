import unittest

from ..Miner import Miner

class TestMiner(unittest.TestCase):
    pass

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
