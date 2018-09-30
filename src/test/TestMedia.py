import unittest

from ..Media import Media

class TestMedia(unittest.TestCase):

    audio_test_1 = 'assets/audio/Dark_Step.mp3'
    audio_test_2 = 'assets/audio/Doll_Dancing.mp3'
    audio_test_3 = 'assets/audio/Drizzle_to_Downpour.mp3'
    audio_test_4 = 'assets/audio/Fur_Elise_by_Beethoven.mp3'
    audio_test_5 = 'assets/audio/Toccata_in_D_minor_by_Bach.mp3'
    unkown_audio = 'assets/audio/Unkown.mp3'

    def test_load_mp3(self):
        media = Media()
        media.load(self.audio_test_2)
        self.assertEqual(media.get_title(), 'Doll Dancing')
        self.assertEqual(media.get_artists(), ['Puddle of Inifinty'])
        self.assertEqual(media.get_album(), 'YouTube Audio Library')
        self.assertEqual(media.get_genres(), ['Cinematic'])
        self.assertEqual(media.get_length(), '2:23')

    def test_error_load(self):
        media = Media()
        self.assertRaises(FileNotFoundError, media.load, 'assets/audio/fake_audio.mp3')

    def test_load_missing_tags(self):
        media = Media()
        media.load(self.unkown_audio)
        self.assertEqual(media.get_genres(), ['Unkown Genre'])


    def test_set_delete_title(self):
        media = Media()
        media.load(self.audio_test_3)
        media.set_title('New Title')
        self.assertEqual(media.get_title(), 'New Title')
        media.delete_title()
        self.assertEqual(media.get_title(), 'Unkown Song')

    def test_add_delete_artists(self):
        media = Media()
        media.load(self.audio_test_1)
        media.add_artist('A')
        self.assertEqual(media.get_artists(), ['Silent Partner', 'A'])
        media.delete_artist('Silent Partner')
        self.assertEqual(media.get_artists(), ['A'])
        self.assertRaises(ValueError, media.delete_artist, 'Silent Partner')
        media.delete_artist('A')
        self.assertEqual(media.get_artists(), ['Unkown Artist'])
        media.add_artist('Silent Partner')
        self.assertEqual(media.get_artists(), ['Silent Partner'])

    def test_set_delete_album(self):
        media = Media()
        media.load(self.audio_test_1)
        media.set_album('Original Album')
        self.assertEqual(media.get_album(), 'Original Album')
        media.delete_album()
        self.assertEqual(media.get_album(), 'Unkown Album')

    def test_add_delete_genres(self):
        media = Media()
        media.load(self.audio_test_1)
        media.add_genre('Dark')
        self.assertEqual(media.get_genres(), ['Dance & Electronic', 'Dark'])
        media.delete_genre('Dance & Electronic')
        self.assertEqual(media.get_genres(), ['Dark'])
        self.assertRaises(ValueError, media.delete_genre, 'Dark & Electronic')
        media.delete_artist('Dark')
        self.assertEqual(media.get_genres(), ['Unkown Genre'])
        media.add_genre('Dance & Electronic')
        self.assertEqual(media.get_genres(), ['Dance & Electronic'])

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMedia)

    unittest.TextTestRunner(verbosity=2).run(suite)
