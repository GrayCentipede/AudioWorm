from mutagen.mp3 import EasyMP3 as MP3
from mutagen import MutagenError

from math import floor

class Media(object):

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
        self.title = 'Unknown Song'
        self.artists = ['Unknown Artist']
        self.album = 'Unknown Album'
        self.genres = ['Unknown Genre']
        self.length = self.path = ''

    def load(self, filename):
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
            if ('year' in tags):
                self.set_year(tags['year'][0])
            if ('track' in tags):
                self.set_track(tags['track'][0])

            self.path = filename
            self.set_length(tags.info.length)

        except MutagenError:
            raise FileNotFoundError('File not found: ' + str(filename))

    def set_title(self, new_title):
        self.title = new_title

    def get_title(self):
        return self.title

    def delete_title(self):
        self.title = 'Unknown Song'

    def add_artist(self, new_artist):
        if ('Unknown Artist' in self.artists):
            self.artists.pop()
            self.artists.append(new_artist)
        else:
            self.artists.append(new_artist)

    def get_artists(self):
        return self.artists

    def delete_artist(self, artist):
        try:
            self.artists.remove(artist)
            if (len(self.artists) == 0):
                self.artists.append('Unknown Artist')
        except ValueError:
            raise ValueError('Artist not found in media file: ' + str(artist))

    def set_album(self, new_album):
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
