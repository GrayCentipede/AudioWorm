"""
A class for testing the miner called TestMiner.
"""

# Unit testing.
import unittest

# Ignore warnings.
import warnings

# Checking files.
import os

# Miner class.
from ..Miner import Miner

class TestMiner(unittest.TestCase):
    
    # The path where the test files are allocated.
    path = 'assets/audio/'

    # The absolute path of the directory where the project is running.
    pre  = os.path.dirname(os.path.abspath(__file__))

    # The absoulte path of the test files.
    test_path = pre + '/' + path

    # The test miner.
    test_miner = Miner(test_path)

    def test_mine(self):
        """
        Tests the miner's method mine.
        """
        self.test_miner.mine()
        files = self.test_miner.get_files()
        acc   = self.test_miner.get_accepted_formats()

        # Checks that every file with an accepted format is properly obtained.
        for root, dirs, files in os.walk(self.test_path):
            for f in files:
                f_name, f_ext = os.path.splitext(f)
                if (f_ext in acc):
                    abs_path_f = root + f
                    print(abs_path_f)
                    self.assertTrue(abs_path_f in files)


if __name__ == '__main__':
    unittest.main()
