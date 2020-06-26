"""
A class for the Data Access Object (DAO) called Manager.
To generate HTML documentation for this module use the command:

    pydoc -w src.Manager

"""

# Handle database queries and connections.
import sqlite3

# Creating, deleting the database file.
import os

# Handle errors and exceptions
import errno

class Manager(object):
    """
    Manager is the one who handles everything related to the database:
    creation, deletion and queries.
    """

    # The path to the file where the database is allocated. Hard Coded.
    database_path = './sql/audioworm.db'

    # SQL path. Hard Coded.
    sql_path      = './sql/rolas.sql'

    def create_database(self, clean = False, recreate = False):
        """
        Creates the file where the database will be allocated.
        :param clean: boolean for a clean installation of the database.
            If True and the database already exists, then all of the 
            database contents are deleted, leaving the database clean.
        :param recreate: boolean for a recreation of the database file.
            If True and the database file exists, then the file is deleted
            and created again.
        """
        conn = sqlite3.connect(self.database_path)

        # Checks if the database file already exists.
        if (os.path.isfile(self.database_path)):
            # If it is a clean installation then clean the database.
            if clean:
                self.clean_database()
        else:
            # If the file needs to be recreated then delete it.
            if recreate:
                self.delete_database()
                
            # Loads the sql file contents.
            f = open(sql_path, 'r')
            c = f.read()
            # Executes and creates the database.
            conn.executescript(c)

        conn.close()

    def clean_database(self):
        """
        Deletes the current contents of the database, leaving the 
        database clean.
        """
        # If the database file doesn't exist then raise an exception.
        if (os.path.isfile(self.database_path):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    self.database_path)

        # Cleans the database.
        conn = sqlite3.connect('./sql/audioworm.db')
        c    = conn.cursor()

        c.execute('DELETE FROM performers')
        c.execute('DELELE FROM people')
        c.execute('DELETE FROM groups')
        c.execute('DELETE FROM albums')
        c.execute('DELETE FROM songs')
        c.execute('DELETE FROM playlists')
            
        conn.commit()
        conn.close()

            
    def delete_database(self):
        """
        Deletes the file where the database is allocated.
        """
        # If the database file doesn't exist then raise an exception.
        if (os.path.isfile(self.database_path):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    self.database_path)

        # Delete the file.
        os.unlink(self.database_path)
