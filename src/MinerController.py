from pathlib import Path
import os

from .Miner import Miner
from .Manager import Manager

class MinerController(object):

    instancer = None
    miner = None
    manager = None

    def __init__(self, instancer):
        self.instancer = instancer
        self.miner = Miner('audioworm')

    def load_miner(self):
        home = str(Path.home())
        self.miner.load_db(os.path.abspath(home + '/Music'))
        self.miner.sort_medias()
        self.manager = Manager()

    def add_rows(self):
        self.instancer.songs_liststore.clear()
        result = self.manager.get_all_songs()
        for row in result:
            song = row[0]
            performer = row[1]
            album = row[2]
            track = '' if row[3] == 'null' else str(row[3])
            year = '' if row[4] == 'null' else str(row[4])
            genre = row[5]
            path = row[6]
            performer_id = row[7]
            performer_type = row[8]
            album_id = row[9]
            song_id = row[10]
            self.instancer.songs_liststore.append([song, performer, album, track,
                                                   year, genre, path, performer_id,
                                                   performer_type, album_id, song_id])
