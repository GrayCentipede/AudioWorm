import unittest

from ..QueryCompiler import QueryCompiler

class TestQueryCompiler(unittest.TestCase):
    pass

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueryCompiler)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
