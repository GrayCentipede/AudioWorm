import unittest

from ..QueryCompiler import QueryCompiler

class TestQueryCompiler(unittest.TestCase):

    def test_search_artists(self):
        compiler = QueryCompiler()
        search_string = 'Artist: Arctic Monkeys'
        compiler.compile(search_string)
        self.assertEqual(compiler.get_artists(), ['Arctic Monkeys'])
        search_string = "Artist: (\[What price, wonderland?\], \[L'indécis\])"
        compiler.compile(search_string)
        self.assertEqual(compiler.get_artists(), ['What price, wonderland?', "L\'indécis"])
        search_string = '''Artist: \['Weird' "Artists"\]'''
        compiler.compile(search_string)
        self.assertEqual(compiler.get_artists(), ['\'Weird\' \"Artist\"'])

    def test_search_songs(self):
        compiler = QueryCompiler()
        search_string = 'Song: Mr Blue Sky'
        compiler.compile(search_string)
        self.assertEqual(compiler.get_songs(), ['Mr Blue Sky'])
        search_string = "Song: (\[One, Two Step (Sam Gelliatery Remix)\], \[Isn't she lovely\])"
        compiler.compile(search_string)
        self.assertEqual(compiler.get_songs(), ['One, Two Step (Sam Gelliatery Remix)', 'Isn\'t she lovely'])
        search_string = '''Song: \['Weird' "Song"\]'''
        compiler.compile(search_string)
        self.assertEqual(compiler.get_songs(), ['\'Weird\' \"Song\"'])

    def test_search_albums(self):
        compiler = QueryCompiler()
        search_string = 'Album: Favourite Worst Nightmare'
        compiler.compile(search_string)
        self.assertEqual(compiler.get_albums(), ['Favourite Worst Nightmare'])
        search_string = "Song: (\[Nameless, Faceless\], \[Untitled '91\], \[V.S.\])"
        compiler.compile(search_string)
        self.assertEqual(compiler.get_albums(), ['Nameless, Faceless', 'Untitled \'91', 'V.S.'])
        search_string = '''Song: \['Weird' "Album"\]'''
        compiler.compile(search_string)
        self.assertEqual(compiler.get_albums(), ['\'Weird\' \"Album\"'])

    def test_invalid_query(self):
        compiler = QueryCompiler()
        search_string = 'Made_Up_Field: The Marías'
        self.assertRaises(SyntaxError, compiler.compile, search_string)
        search_string = 'Artist: AC/DC)'
        self.assertRaises(SyntaxError, compiler.compile, search_string)
        search_string = 'Artist: (Los Blenders'
        self.assertRaises(SyntaxError, compiler.compile, search_string)
        search_string = 'Song: \[Gutter Girl'
        self.assertRaises(SyntaxError, compiler.compile, search_string)
        search_string = 'Song: Gutter Girl\]'
        self.assertRaises(SyntaxError, compiler.compile, search_string)

    def test_search_multiple(self):
        compiler = QueryCompiler()
        search_string = 'Artist: A1. Song: (S1, S2). Persons: (P1, \[P"2"\])'
        compiler.compile(search_string)
        self.assertEqual(compiler.get_artists(), ['A1'])
        self.assertEqual(compiler.get_songs(), ['S1', 'S2'])
        self.assertEqual(compiler.get_persons(), ['P1', 'P\"2\"'])
        self.assertEqual(compiler.get_albums(), [])

    def test_query(self):
        pass


if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueryCompiler)

    unittest.TextTestRunner(verbosity=2).run(suite)
