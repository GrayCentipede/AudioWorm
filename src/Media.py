from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3, APIC
from mutagen import MutagenError

from PIL import Image

from math import floor

"""
A class for the MP3 files called Media.
To generate HTML documentation for this module use the command:

    pydoc -w src.Media

"""

class Media(object):
    """
    Media is the one who stores all the tags of an MP3 file
    It encapsulates:
        title -  The media's title
        artists - The media's artists
        album - The media's album
        genres - The media's genre
        length - The media's length
        year - The media's year
        track - The media's track
        path - The media's path on the system
        tags - The media's tag
    """

    title = None
    artists = None
    album = None
    genres = None
    length = None
    year = None
    track = None
    path = None
    tags = None

    def __init__(self):
        """
        Creates a Media with the default contents of an MP3 files.
        """

        self.title = 'Unknown Song'
        self.artists = ['Unknown Artist']
        self.album = 'Unknown Album'
        self.genres = ['Unknown Genre']
        self.length = self.path = self.track = self.year = ''

    def load(self, filename):
        """
        Loads a Media with all the tags of a given MP3

        :param filename: The path of the MP3 file
        """

        try:
            tags = MP3(filename)

            if ('title' in tags):
                self.set_title(tags['title'][0])
            if ('artist' in tags):
                for artist in tags['artist']:
                    self.add_artist(artist)
            if ('album' in tags):
                self.set_album(tags['album'][0])
            if ('genre' in tags):
                for genre in tags['genre']:
                    self.add_genre(genre)
            if ('date' in tags):
                self.set_year(tags['date'][0])
            if ('tracknumber' in tags):
                self.set_track(tags['tracknumber'][0])

            self.path = filename
            self.set_length(tags.info.length)

        except MutagenError:
            raise FileNotFoundError('File not found: ' + str(filename))

    def set_title(self, new_title):
        """
        Changes the title for the media

        :param new_title: The new title
        """

        self.title = new_title

    def get_title(self):
        """
        Gets the title of a Media

        :return: The media's title
        """

        return self.title

    def delete_title(self):
        """
        Deletes the title of the media and sets it to: 'Unknown Song'
        """

        self.title = 'Unknown Song'

    def add_artist(self, new_artist):
        """
        Adds a new artist for the media

        :param new_artist: The new artist
        """

        if ('Unknown Artist' in self.artists):
            self.artists.pop()
            self.artists.append(new_artist)
        else:
            self.artists.append(new_artist)

    def get_artists(self):
        """
        Gets the artists of a Media

        :return: The media's artists
        """

        return self.artists

    def get_artists_str(self):
        """
        Gets the artists of a Media in string format

        :return: The media's artists in a string format
        """

        artists = self.artists
        n = len(artists)

        if (n == 1):
            return str(artists[0])

        i = 0
        string = ''
        for artist in artists:
            if (i + 1 == n):
                string += str(artist)
            else:
                string += str(artist) +  ', '

        return string

    def delete_artist(self, artist):
        """
        Deletes an artists in a media, if there are no more artists then it is set as 'Unknown Artist'
        """

        try:
            self.artists.remove(artist)
            if (len(self.artists) == 0):
                self.artists.append('Unknown Artist')
        except ValueError:
            raise ValueError('Artist not found in media file: ' + str(artist))

    def set_album(self, new_album):
        """
        Changes the album for the media

        :param new_album: The new album's name
        """

        self.album = new_album

    def get_album(self):
        return self.album

    def delete_album(self):
        self.album = 'Unknown Album'

    def add_genre(self, new_genre):
        if ('Unknown Genre' in self.genres):
            self.genres.pop()
            self.genres.append(new_genre)
        else:
            self.genres.append(new_genre)

    def get_genres(self):
        return self.genres

    def get_genres_str(self):
        genres = self.genres
        n = len(genres)

        if (n == 1):
            return str(genres[0])

        i = 0
        string = ''
        for genre in genres:
            if (i + 1 == n):
                string += str(genre)
            else:
                string += str(genre) +  ', '

        return string

    def delete_genre(self, genre):
        try:
            self.genres.remove(genre)
            if (len(self.genres) == 0):
                self.genres.append('Unknown Genre')
        except ValueError:
            raise ValueError('Genre not found in media file: ' + str(genre))

    def set_year(self, year):
        self.year = year

    def get_year(self):
        return self.year

    def set_track(self, track):
        self.track = track

    def get_track(self):
        return self.track

    def set_length(self, seconds):
        minute_w_sec = seconds / 60
        minute = floor(minute_w_sec)
        decimals = minute_w_sec % 1
        seconds = floor(decimals * 60)
        self.length = str(minute) + ':' + str(seconds)

    def get_length(self):
        return self.length

    def get_path(self):
        return self.path

    def get_album_cover_of_file(filename):
        image_bytes = None
        audio = ID3(filename)
        for key in audio.keys():
            if ('APIC' in key):
                image_bytes = bytearray(audio[key].data)
                return image_bytes
        return None
