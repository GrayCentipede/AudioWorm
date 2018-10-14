import vlc

class Player(object):

    loaded = False

    def __init__(self):
        self.player = None

    def load(self, file):
        self.player = vlc.MediaPlayer(file)
        self.loaded = True

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        if (self.loaded):
            self.player.stop()

    def is_loaded(self):
        return self.loaded
