from pathlib import Path
import os

from .Miner import Miner
from .Manager import Manager

"""
A class for the controller of the miner that the UI will be using.
To generate HTML documentation for this module use the command:

    pydoc -w src.MinerController

"""

class MinerController(object):
    """
    Media is the one who stores all the tags of an MP3 file
    It encapsulates:
        instancer - The window that instanced the controller
        miner - The controller's miner
        manager - The controller's manager
    """

    instancer = None
    miner = None
    manager = None

    def __init__(self, instancer):
        """
        Creates a controller that creates or reads from the database.

        :param instancer: The window that instanced the controller
        """

        self.instancer = instancer
        self.miner = Miner('audioworm')

    def load_miner(self):
        """
        Loads all the MP3 files from the '~/Music' directory
        """

        home = str(Path.home())
        self.miner.load_db(os.path.abspath(home + '/Music'))
        self.miner.sort_medias()
        self.manager = Manager()

    def add_rows(self):
        """
        Appends all the medias information to the window's liststore
        """

        self.instancer.songs_liststore.clear()
        result = self.manager.get_all_songs()
        for row in result:
            song = row[0]
            performer = row[1]
            album = row[2]
            year = '' if row[3] == 'null' else str(row[3])
            track = '' if row[4] == 'null' else str(row[4])
            genre = row[5]
            path = row[6]
            performer_id = row[7]
            performer_type = row[8]
            album_id = row[9]
            song_id = row[10]
            self.instancer.songs_liststore.append([song, performer, album, track,
                                                   year, genre, path, performer_id,
                                                   performer_type, album_id, song_id])
    def filter(self, rows):
        """
        Appends all the medias information that fulfilled the condition to the window's liststore

        :param rows: The medias that fulfilled the condition
        """
        
        self.instancer.songs_liststore.clear()
        for row in rows:
            song = row[0]
            performer = row[1]
            album = row[2]
            year = '' if row[3] == 'null' else str(row[3])
            track = '' if row[4] == 'null' else str(row[4])
            genre = row[5]
            path = row[6]
            performer_id = row[7]
            performer_type = row[8]
            album_id = row[9]
            song_id = row[10]
            self.instancer.songs_liststore.append([song, performer, album, track,
                                                   year, genre, path, performer_id,
                                                   performer_type, album_id, song_id])
