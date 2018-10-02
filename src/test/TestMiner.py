import unittest
import os

from ..Miner import Miner

class TestMiner(unittest.TestCase):
    path = './src/test/assets/audio/'
    miner = None

    def setUp(self):
        self.miner = Miner('audioworm_test')
        self.miner.load_db(self.path)

    def test_error_load(self):
        decoy_miner = Miner('audioworm_test')
        self.assertRaises(FileNotFoundError, decoy_miner.load_db, './src/test/assets/non-existant-dir/')

    def test_songs(self):
        query = 'SELECT title FROM rolas'
        songs = []
        songs.append('Dark Step')
        songs.append('Doll Dancing')
        songs.append('Drizzle to Downpour')
        songs.append('Fur Elise (by Beethoven)')
        songs.append('Toccata in D minor (by Bach)')
        songs.append('Unknown Song')
        rows = self.miner.send_query(query)
        for row in rows:
            self.assertTrue(row[0] in songs)

    def test_performers(self):
        query = 'SELECT name FROM performers'
        performers = []
        performers.append('Silent Partner')
        performers.append('Puddle of Infinity')
        performers.append('Beethoven')
        performers.append('Bach')
        performers.append('Unknown Artist')
        rows = self.miner.send_query(query)
        for row in rows:
            self.assertTrue(row[0] in performers)

    def test_albums(self):
        query = 'SELECT name FROM albums'
        albums = []
        albums.append('YouTube Audio Library')
        albums.append('Unknown Album')
        rows = self.miner.send_query(query)
        for row in rows:
            self.assertTrue(row[0] in albums)


if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)
    unittest.TextTestRunner(verbosity=2).run(suite)
    os.unlink('./sql/audioworm_test.db')
