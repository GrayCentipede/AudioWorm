import sqlite3
import os
import glob

from .Media import Media

"""
A class for the MP3 files miner called Miner.
To generate HTML documentation for this module use the command:

    pydoc -w src.Miner

"""

class Miner(object):
    """
    Media is the one who stores all the tags of an MP3 file
    It encapsulates:
        database_path - The database's path
        connection - The connection to the database
        cursor - The cursor of the connection
        listener - A listener
        medias - The list of medias
    """

    database_path = None
    connection = None
    cursor = None
    listener = None
    medias = []

    def __init__(self, db_name):
        """
        Creates a Miner with an established connection to the database.
        In case it doesn't exist then it creates it from the sql file that contains the data definition
        language (DDL).

        :param db_name: The database name
        """

        self.database_path = './sql/' + db_name + '.db'
        self.connection = sqlite3.connect(self.database_path)
        f_1 = open('./sql/rolas.sql', 'r')
        content = f_1.read()
        f_2 = open(self.database_path)
        if (os.stat(self.database_path).st_size == 0):
            self.connection.executescript(content)

    def get_medias(self):
        """
        Returns all the medias that have been loaded.

        :return: The medias that have been loaded
        """

        return self.medias

    def load_db(self, directory):
        """
        Gets all the MP3 files of the given directory and it seeds the database with their information.

        :param directory: The directory where the MP3 can be found
        """

        if (not os.path.isdir(directory)):
            raise FileNotFoundError('Directory ' + directory + ' not found.')

        files = glob.glob(directory + '/**/*.mp3', recursive = True)
        for file in files:
            m = Media()
            m.load(file)
            self.medias.append(m)

        self.seed_db()

    def seed_db(self):
        """
        Seeds the database with the media's information
        """

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
        """
        Gets the performer's id of a given artist.

        :param artist: The artist's name
        :return: None if it doesn't exist, the performer's id in other case
        """

        search_query = 'SELECT id_performer FROM performers WHERE name = \'{}\''.format(artist)
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return rows[0][0]

        return None

    def insert_performer(self, artist):
        """
        Inserts a performer in the database

        :param artist: The artist to insert
        """

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
        """
        Gets the album's id of a title.

        :param album_title: The album's title
        :return: None if it doesn't exist, the album's id in other case
        """

        search_query = 'SELECT id_album FROM albums WHERE name = \'{}\''.format(album_title)
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return rows[0][0]

        return None

    def insert_album(self, album, path, album_year):
        """
        Inserts an album in the database

        :param album: The album to insert
        :param path: The album's path
        :param album_year: The album's year
        """

        search_query = 'SELECT id_album FROM albums'
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) == 0):
            new_id = str(0)
        else:
            new_id = str(rows[-1][0] + 1)

        year = 'null' if album_year is '' else str(album_year)
        insert_query = 'INSERT INTO albums VALUES ({}, \'{}\', \'{}\', {})'.format(new_id, path, album, year)
        self.connection.execute(insert_query)
        self.connection.commit()
        return new_id

    def get_song_id(self, song, id_performer, id_album):
        """
        Gets the song's id of a title.

        :param song: The song's title
        :param id_performer: The id of the song's performer
        :param id_album: The id of the song's album
        :return: None if it doesn't exist, the song's id in other case
        """

        search_query = 'SELECT id_rola FROM rolas WHERE '
        search_query += 'id_performer = ? '
        search_query += 'AND id_album = ? '
        search_query += 'AND title = ?'
        cursor = self.connection.execute(search_query, (id_performer, id_album, song))
        rows = cursor.fetchall()
        if (len(rows) > 0):
            return rows[0][0]

        return None

    def insert_song(self, id_performer, id_album, path, song, album_track, album_year, genre):
        """
        Inserts a song in the database

        :param id_performer: The id of the song's performer
        :param id_album: The id of the song's album
        :param path: The song's path
        :param song: The song's title
        :param album_track: The song's track
        :param album_year: The album's year
        :param genre: The song's genre
        """

        search_query = 'SELECT id_rola FROM rolas'
        cursor = self.connection.execute(search_query)
        rows = cursor.fetchall()

        if (len(rows) == 0):
            new_id = str(0)
        else:
            new_id = str(rows[-1][0] + 1)

        year = 'null' if album_year is '' else str(album_year)
        track = 'null' if album_track is '' else str(album_track)
        insert_query = 'INSERT INTO rolas VALUES '
        insert_query += '(?,'
        insert_query += ' ?,'
        insert_query += ' ?,'
        insert_query += ' ?,'
        insert_query += ' ?,'
        insert_query += ' ?,'
        insert_query += ' ?,'
        insert_query += ' ?)'

        self.connection.execute(insert_query,
                                (new_id, id_performer, id_album, path, song, track, year, genre))
        self.connection.commit()

    def set_listener(self, f):
        """
        Sets a listener

        :param f: The function that will be the listener
        """

        self.listener = f

    def sort_medias(self):
        """
        Sort the medias by artist.
        """

        self.medias = sorted(self.medias, key = lambda m: m.get_artists())

    def send_query(self, query):
        """
        Sends a query to the database.
        """

        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def dump_db(self):
        """
        Deletes the database
        """

        os.unlink(self.database_path)
