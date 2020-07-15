"""
A class for testing the DAO called TestManager.
"""

# Unit testing.
import unittest

# Ignoring warnings.
import warnings

# Checking files.
import os

# SQLITE3 transactions.
import sqlite3

# Manager class
from ..Manager import Manager

class TestManager(unittest.TestCase):

    # The test database.
    test_path    = './sql/test.db'

    # The test manager.
    test_manager = Manager('test')

    def test_build_database(self):
        """
        Tests the manager's method build_database with 
        no extra arguments.
        """
        # Check there is no database file already.
        self.assertFalse(os.path.isfile(self.test_path))
        # Build the database.
        self.test_manager.build_database()
        # Check there is a database file.
        self.assertTrue(os.path.isfile(self.test_path))

        # Deletes the database created.
        os.unlink(self.test_path)

    def test_build_database_clean(self):
        """
        Tests the manager's method build_database with
        the argument 'clean'.
        """
        # Check if there is no database file already and create it.
        self.assertFalse(os.path.isfile(self.test_path))
        self.test_manager.build_database()
        self.assertTrue(os.path.isfile(self.test_path))

        # Insert some useless data in the database.
        conn = sqlite3.connect(self.test_path)
        c    = conn.cursor()

        query  = 'INSERT INTO performers(id_type, name)'
        query += ' VALUES(?, ?)'

        c.execute(query, (0, 'TEST'))
        
        conn.commit()

        # Clean database.
        self.test_manager.build_database(clean = True)
        # Check it is, indeed, empty.
        query = 'SELECT * FROM performers'
        res   = c.execute(query).fetchone()
        self.assertEqual(res, None)

        # Deletes the database created.
        os.unlink(self.test_path)

    def test_insert_performer(self):
        """
        Tests the manager's method insert_performer.
        """
        # Builds database and inserts performer.
        self.test_manager.build_database()
        self.test_manager.insert_performer('Test Artist')

        # Check if it was inserted.
        conn = sqlite3.connect(self.test_path)
        c    = conn.cursor()
        
        query = 'SELECT * FROM performers WHERE name=?'
        res   = c.execute(query, ('Test Artist',)).fetchone()
        self.assertFalse(res is None)

        # Deletes the created database.
        os.unlink(self.test_path)

    def test_insert_person(self):
        """
        Tests the manager's method insert_person.
        """
        pass

    def test_insert_group(self):
        """
        Tests the manager's method insert_group.
        """
        pass

    def test_insert_album(self):
        """
        Tests the manager's method insert_album.
        """
        pass

    def test_insert_song(self):
        """
        Tests the manager's method insert_song.
        """
        pass

    def test_insert_playlist(self):
        """
        Tests the manager's method insert_playlist.
        """
        pass
        


if __name__ == '__main__':
    unittest.main()
