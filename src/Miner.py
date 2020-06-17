"""
A class for the miner, responsible of mining all the music files.
To generate HTML documentation for this module use the command:

    pydoc -w src.Miner

"""

# Moving through directories
import os

class Miner(object):
    """
    Class for a miner.
    """

    # The base directory.
    directory = None

    # Mined files.
    files = None

    # Accepted music formats. Hard coded.
    acc_formats = ['.mp3']

    def __init__(self, directory):
        """
        Construct a miner.
        :param directory: The base directory that contains all the music files.
        """
        self.directory = directory
        self.files     = []

    def mine(self):
        """
        Mines all the music files contained in the base directory.
        """
        for root, dirs, files in os.walk(self.directory):
            for f in files:
                f_name, f_ext = os.path.splitext(f)
                if (f_ext in self.acc_formats):
                    abs_path_f = root + '/' + f
                    self.files.append(abs_path_f)
