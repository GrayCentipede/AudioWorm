import unittest

from ..Media import Media

class TestMedia(unittest.TestCase):
    pass

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMedia)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
