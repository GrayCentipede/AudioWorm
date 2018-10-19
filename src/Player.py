import vlc
from math import floor

"""
A class for the music player.
To generate HTML documentation for this module use the command:

    pydoc -w src.Player

"""

class Player(object):
    """
    Player is the one the plays the music.
    It encapsulates:
        loaded - Tells whether or not a file has been loaded
    """

    loaded = False

    def __init__(self):
        """
        Creates a music player
        """

        self.player = None

    def load(self, file):
        """
        Loads the player with a file.

        :param file: The file to load
        """

        self.player = vlc.MediaPlayer(file)
        self.loaded = True

    def play(self):
        """
        Plays the song.
        """

        self.player.play()

    def pause(self):
        """
        Pauses the song.
        """

        self.player.pause()

    def stop(self):
        """
        Stops the song if loaded.
        """

        if (self.loaded):
            self.player.stop()

    def is_loaded(self):
        """
        Return whether or not the song has been loaded.

        :return: Whether or not the song has been loaded.
        """

        return self.loaded

    def get_length(self):
        """
        Gets the songs length in a format of 'mm:ss' (minutes, seconds)
        """

        miliseconds = self.player.get_length() / 1000
        mm, ss = divmod(miliseconds, 60)
        return "%02d:%02d" % (mm,ss)
