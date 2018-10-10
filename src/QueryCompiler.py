class QueryCompiler(object):

    artists = None
    songs = None
    albums = None
    persons = None
    known_fields = ['Artist', 'Song', 'Person', 'Album']

    def __init__(self):
        self.artists = []
        self.songs = []
        self.albums = []
        self.persons = []

    def compile(self, search_string):
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
        if (field == 'Artist'):
            self.artists = contents
        elif (field == 'Song'):
            self.songs = contents
        elif (field == 'Person'):
            self.persons = contents
        elif (field == 'Album'):
            self.albums = contents
        else:
            raise ValueError('Field was not recognized')

    def parse(self, field, content):
        field = field.strip()
        if field not in self.known_fields:
            e = 'Field '+ field +' is not accepted'
            raise ValueError(e)

        contents = self.parse_content(content.strip())
        self.set_content(field, contents)

    def get_artists(self):
        return self.artists

    def get_songs(self):
        return self.songs

    def get_albums(self):
        return self.albums

    def get_persons(self):
        return self.persons

    def get_query(self):
        pass
