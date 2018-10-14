from pathlib import Path
import os

from .Miner import Miner

class MinerController(object):

    instancer = None
    miner = None

    def __init__(self, instancer):
        self.instancer = instancer
        self.miner = Miner('audioworm')

    def load_miner(self):
        home = str(Path.home())
        self.miner.load_db(os.path.abspath(home + '/Music'))
        self.miner.sort_medias()

    def add_rows(self):
        medias = self.miner.get_medias()
        for m in medias:
            info = [m.get_title(), m.get_artists_str(), m.get_album(),
                    m.get_track(), m.get_year(), m.get_genres_str(), m.get_path()]
            self.instancer.songs_liststore.append(info)
