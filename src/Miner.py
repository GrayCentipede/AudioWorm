import sqlite3
import os
import glob

from .Media import Media

class Miner(object):
    database_path = None
    connection = None
    cursor = None
    medias = []

    def __init__(self, db_name):
        self.database_path = './sql/' + db_name + '.db'
        self.connection = sqlite3.connect(self.database_path)
        f_1 = open('./sql/rolas.sql', 'r')
        content = f_1.read()
        f_2 = open(self.database_path)
        if (os.stat(self.database_path).st_size == 0):
            self.connection.executescript(content)

    def load_db(self, directory):
        if (not os.path.isdir(directory)):
            raise FileNotFoundError('Directory ' + directory + ' not found.')

        files = glob.glob(directory + '/**/*.mp3', recursive = True)
        for file in files:
            m = Media()
            m.load(file)
            self.medias.append(m)

        self.seed_db()

    def seed_db(self):
        for media in self.medias:
            path = media.get_path()
            year = media.get_year()
            track = media.get_track()
            title = media.get_title()

            ### Handles Artists ###
            for artist in media.get_artists():
                artist_id = self.get_performer_id(artist)
                if (artist_id is None):
                    artist_id = self.insert_performer(artist)

            ### Handles Albums ###
            album_id = self.get_album_id(media.get_album())
            if (album_id is None):
                album_id = self.insert_album(media.get_album(), path, year)

            ### Handles Song ###
            song_id = self.get_song_id(media.get_title(), artist_id, album_id)
            if (song_id is None):
                genre = ';'.join(media.get_genres())
                self.insert_song(artist_id, album_id, path, title, track, year, genre)

    def get_performer_id(self, artist):
        search_query = 'SELECT id_performer FROM performers WHERE name = \'{}\''.format(artist)
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return rows[0][0]

        return None

    def insert_performer(self, artist):
        search_query = 'SELECT id_performer FROM performers'
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) == 0):
            new_id = str(0)
        else:
            new_id = str(rows[-1][0] + 1)

        insert_query = 'INSERT INTO performers VALUES ({}, 2, \'{}\')'.format(new_id, artist)
        self.connection.execute(insert_query)
        self.connection.commit()
        return new_id

    def get_album_id(self, album_title):
        search_query = 'SELECT id_album FROM albums WHERE name = \'{}\''.format(album_title)
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return rows[0][0]

        return None

    def insert_album(self, album, path, album_year):
        search_query = 'SELECT id_album FROM albums'
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) == 0):
            new_id = str(0)
        else:
            new_id = str(rows[-1][0] + 1)

        year = 'null' if album_year is None else str(album_year)
        insert_query = 'INSERT INTO albums VALUES ({}, \'{}\', \'{}\', {})'.format(new_id, path, album, year)
        self.connection.execute(insert_query)
        self.connection.commit()
        return new_id

    def get_song_id(self, song, id_performer, id_album):
        search_query = 'SELECT id_rola FROM rolas WHERE '
        search_query += 'id_performer = {} '.format(id_performer)
        search_query += 'AND id_album = {} '.format(id_album)
        search_query += 'AND title = \'{}\''.format(song)
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return rows[0][0]

        return None

    def insert_song(self, id_performer, id_album, path, song, album_track, album_year, genre):
        search_query = 'SELECT id_rola FROM rolas'
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) == 0):
            new_id = str(0)
        else:
            new_id = str(rows[-1][0] + 1)

        year = 'null' if album_year is None else str(album_year)
        track = 'null' if album_track is None else str(album_track)
        insert_query = 'INSERT INTO rolas VALUES '
        insert_query += '({},'.format(new_id)
        insert_query += ' {},'.format(id_performer)
        insert_query += ' {},'.format(id_album)
        insert_query += ' \'{}\','.format(path)
        insert_query += ' \'{}\','.format(song)
        insert_query += ' {},'.format(track)
        insert_query += ' {},'.format(year)
        insert_query += ' \'{}\')'.format(genre)

        self.connection.execute(insert_query)
        self.connection.commit()

    def send_query(self, query):
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def dump_db(self):
        os.unlink(self.database_path)
