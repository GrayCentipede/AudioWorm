"""
A class for the query compiler.
To generate HTML documentation for this module use the command:

    pydoc -w src.QueryCompiler

"""

class QueryCompiler(object):
    """
    Player is the one the plays the music.
    It encapsulates:
        artists - A list of the artists found in the search query
        albums - A list of the albums found in the search query
        songs - A list of the songs found in the search query
        year - A list of the years found in the search query
        track - A list of the tracks found in the search query
        persons - A list of the persons found in the search query
        group - A list of the groups found in the search query
    """

    artists = None
    albums = None
    songs = None
    year = None
    track = None
    persons = None
    group = None

    known_fields = ['Artist', 'Album', 'Song', 'Year', 'Track', 'Person', 'Group', 'Genre']

    def __init__(self):
        """
        Creates a compiler.
        """

        self.artists = []
        self.albums = []
        self.songs = []
        self.years = []
        self.tracks = []
        self.genres = []
        self.persons = []
        self.groups = []


    def compile(self, search_string):
        """
        Compiles the given search string.

        :param search_string: The string that contains all the entities to search
        """

        special_chars = ['á', 'é', 'í', 'ó', 'ú']
        fields = []
        contents = []

        i = 0
        j = 0

        found_field_name_end = False
        found_field_content_end = False
        found_parentheses_init = False
        found_parentheses_end = True
        found_special_input_init = False
        found_special_input_end = True

        field_name_start = 0
        field_name_end = 0
        field_content_start = 0
        field_content_end = 0

        jump = False

        current_index = 0
        for char in search_string:
            if (jump):
                jump = False
                current_index += 1
                continue

            if (char == '.' and found_parentheses_end and found_special_input_end):
                field_content_end = current_index
                found_field_name_end = found_field_content_end = found_parentheses_init = False
                found_special_input_init = False
                found_parentheses_end = found_special_input_end = True
                jump = True
                field_name_start = current_index + 1
                contents.append(search_string[field_content_start:field_content_end])

            elif (not found_field_name_end):
                if (char == ':'):
                    found_field_name_end = True
                    field_name_end = current_index
                    field_content_start = current_index + 1
                    fields.append(search_string[field_name_start: field_name_end])

                elif not char.isalpha() and char not in special_chars:
                    e = 'Invalid Query: Field name must only have aplhabetic characters.'
                    e += 'Invalid: ' + str(char)
                    raise SyntaxError(e)

            else:
                if found_special_input_end:
                    if (char == '('):
                        found_parentheses_init = True
                        found_parentheses_end = False

                    elif (char == ')'):
                        if not found_parentheses_init:
                            raise SyntaxError('Invalid Query: Missing parentheses')
                        else:
                            found_parentheses_end = True

                    elif (char == '\\'):
                        next_char = search_string[current_index + 1]
                        if (next_char == '['):
                            found_special_input_init = True
                            found_special_input_end = False
                            jump = True
                        else:
                            raise SyntaxError('Invalid Query: invalid command \\' + next_char)
                else:
                    if (char == '\\'):
                        next_char = search_string[current_index + 1]
                        if (next_char == '['):
                            raise SyntaxError('Invalid Query: invalid command \\' + next_char)
                        elif (next_char == ']'):
                            found_special_input_end = True
                            jump = True


            current_index += 1

        if (search_string[-1] != '.'):
            raise SyntaxError('Invalid Query. Missing dot.')
        elif (found_parentheses_init and not found_parentheses_end):
            raise SyntaxError('Invalid Query. Missing parentheses.')
        elif (found_special_input_init and not found_special_input_end):
            raise SyntaxError('Invalid Query. Missing \\].')

        for i in range(len(fields)):
            self.parse(fields[i], contents[i])

    def parse_content(self, string):
        """
        Parses the string to a list format

        :param string: The string to parse
        :return: A list with the contents of the string
        """

        content = []
        commas_index = []
        in_special_input = False

        current_index = -1
        for char in string:
            current_index += 1
            if char == ',' and not in_special_input:
                commas_index.append(current_index)
            elif (char == '\\'):
                next_char = string[current_index + 1]
                if (next_char == '['):
                    in_special_input = True
                elif (next_char == ']'):
                    in_special_input = False

        if (len(commas_index) == 0):
            content.append(string)
        else:
            for i in range(len(commas_index)):
                if (i == 0):
                    content.append(string[0:commas_index[i]])
                if (i + 1 < len(commas_index)):
                    content.append(string[commas_index[i]+1:commas_index[i+1]])
                else:
                    content.append(string[commas_index[i]+1:])

        filtered_content = []

        for c in content:
            c = c.strip()
            if ('(' in c and c.index('(') == 0):
                c = c[1:]
            if (')' in c and c.index(')') == len(c) - 1):
                c = c[:-1]
            if ('\[' in c):
                c = c[2:-2]

            filtered_content.append(c)

        return filtered_content


    def set_content(self, field, contents):
        """
        Assigns the contents to a field.

        :param field: The field
        :param contents: The contents
        """

        if (field == 'Artist'):
            self.artists = contents
        elif (field == 'Album'):
            self.albums = contents
        elif (field == 'Song'):
            self.songs = contents
        elif (field == 'Year'):
            self.years = contents
        elif (field == 'Track'):
            self.tracks = contents
        elif (field == 'Person'):
            self.persons = contents
        elif (field == 'Group'):
            self.albums = contents
        elif (field == 'Genre'):
            self.genres = contents
        else:
            raise ValueError('Field was not recognized')

    def parse(self, field, content):
        """
        Parses the contents of a string and assigns them to a field

        :param field: The field
        :param content: The contents
        """

        field = field.strip()
        if field not in self.known_fields:
            e = 'Field '+ field +' is not accepted'
            raise ValueError(e)

        contents = self.parse_content(content.strip())
        self.set_content(field, contents)

    def get_artists(self):
        """
        Returns the artists found

        :return: The artists found
        """

        return self.artists

    def get_songs(self):
        """
        Returns the songs found

        :return: The songs found
        """

        return self.songs

    def get_albums(self):
        """
        Returns the albums found

        :return: The albums found
        """

        return self.albums

    def get_persons(self):
        """
        Returns the persons found

        :return: The persons found
        """

        return self.persons

    def get_query(self):
        """
        Returns the search string in a SQL format query.

        :return: The SQL format query
        """
        
        final_query =  'SELECT rolas.title,'
        final_query += '       performers.name,'
        final_query += '       albums.name,'
        final_query += '       rolas.track,'
        final_query += '       rolas.year,'
        final_query += '       rolas.genre,'
        final_query += '       rolas.path,'
        final_query += '       rolas.id_performer,'
        final_query += '       performers.id_type,'
        final_query += '       rolas.id_album,'
        final_query += '       rolas.id_rola '
        final_query += 'FROM rolas JOIN performers JOIN albums '
        final_query += 'WHERE '

        queries = ['rolas.id_performer = performers.id_performer AND rolas.id_album = albums.id_album']

        if (len(self.artists) > 0):
            artist_query = '('
            if (len(self.artists) == 1):
                artist_query += 'performers.name LIKE \'%{}%\')'.format(self.artists[0])
            else:
                i = 0
                for artist in self.artists:
                    if (i + 1 < len(self.artists)):
                        artist_query += 'performers.name LIKE \'%{}%\' OR '.format(artist)
                    else:
                        artist_query += 'performers.name LIKE \'%{}%\')'.format(artist)
                    i += 1

            queries.append(artist_query)

        if (len(self.albums) > 0):
            album_query = '('
            if (len(self.albums) == 1):
                album_query += 'albums.name LIKE \'%{}%\')'.format(self.albums[0])
            else:
                i = 0
                for album in self.albums:
                    if (i + 1 < len(self.albums)):
                        album_query += 'performers.name LIKE \'%{}%\' OR '.format(album)
                    else:
                        album_query += 'performers.name LIKE \'%{}%\')'.format(album)
                    i += 1

            queries.append(album_query)

        if (len(self.songs) > 0):
            song_query = '('
            if (len(self.songs) == 1):
                song_query += 'rolas.title LIKE \'%{}%\')'.format(self.songs[0])
            else:
                i = 0
                for song in self.songs:
                    if (i + 1 < len(self.songs)):
                        song_query += 'rolas.title LIKE \'%{}%\' OR '.format(song)
                    else:
                        song_query += 'rolas.title LIKE \'%{}%\')'.format(song)
                    i += 1

            queries.append(song_query)

        if (len(self.years) > 0):
            year_query = '('
            if (len(self.years) == 1):
                year_query += 'rolas.year LIKE \'%{}%\')'.format(self.years[0])
            else:
                i = 0
                for track in self.years:
                    if (i + 1 < len(self.years)):
                        year_query += 'rolas.year LIKE \'%{}%\' OR '.format(track)
                    else:
                        year_query += 'rolas.year LIKE \'%{}%\')'.format(track)
                    i += 1

            queries.append(year_query)

        if (len(self.tracks) > 0):
            track_query = '('
            if (len(self.tracks) == 1):
                track_query += 'rolas.track LIKE \'%{}%\')'.format(self.tracks[0])
            else:
                i = 0
                for track in self.tracks:
                    if (i + 1 < len(self.tracks)):
                        track_query += 'rolas.track LIKE \'%{}%\' OR '.format(track)
                    else:
                        track_query += 'rolas.track LIKE \'%{}%\')'.format(track)
                    i += 1

            queries.append(track_query)

        if (len(self.genres) > 0):
            genre_query = '('
            if (len(self.genres) == 1):
                genre_query += 'rolas.genre LIKE \'%{}%\')'.format(self.genres[0])
            else:
                i = 0
                for genre in self.genres:
                    if (i + 1 < len(self.genres)):
                        genre_query += 'rolas.genre LIKE \'%{}%\' OR '.format(genre)
                    else:
                        genre_query += 'rolas.genre LIKE \'%{}%\')'.format(genre)
                    i += 1

            queries.append(genre_query)

        return final_query + ' AND '.join(queries) + 'ORDER BY performers.name, albums.name, rolas.track'
