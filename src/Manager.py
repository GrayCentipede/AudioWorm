import sqlite3

"""
A class for the Data Access Object (DAO) called Manager.
To generate HTML documentation for this module use the command:

    pydoc -w src.Manager

"""

class Manager(object):
    """
    Manager is the one who will consult everything to the database
    It encapsulates:
        connection - The connection to the database
    """

    connection = None

    def __init__(self):
        """
        Creates a manager, the connection to the database
        """

        self.connection = sqlite3.connect('./sql/audioworm.db')

    def get_all_songs(self):
        """
        Gets all the songs in the database
        """

        query = 'SELECT rolas.title, performers.name, albums.name, rolas.track, rolas.year, rolas.genre,'
        query += 'rolas.path, rolas.id_performer, performers.id_type, rolas.id_album, rolas.id_rola '
        query += 'FROM rolas JOIN performers JOIN albums '
        query += 'WHERE rolas.id_performer = performers.id_performer AND rolas.id_album = albums.id_album '
        query += 'ORDER BY performers.name, albums.name, rolas.track'
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def get_all_groups(self):
        """
        Gets all the groups in the database
        """

        query = 'SELECT id_group, name FROM groups'
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def get_person(self, performer_name):
        """
        Gets the person given its performe's name

        :param performer_name: The person's stage name
        """

        query = 'SELECT real_name, birth_date, death_date '
        query += 'FROM persons WHERE stage_name = ?'
        cursor = self.connection.execute(query, (performer_name,))
        rows = cursor.fetchall()
        return rows[0]

    def get_group_person_is_in(self, person_id):
        """
        Gets the group a person is in

        :param person_id: The id of the person
        """

        query = 'SELECT groups.id_group FROM performers JOIN groups JOIN in_group '
        query += 'WHERE in_group.id_person = ?'
        cursor = self.connection.execute(query, (person_id,))
        rows = cursor.fetchall()

        if (len(rows) > 0):
            return rows[0]

        return None

    def get_persons_in_group(self, group_name):
        """
        Gets all the persons that are in a group

        :param group_name: The name of the group
        """

        query = 'SELECT in_group.id_group FROM in_group JOIN groups '
        query += 'WHERE groups.name = ?'
        cursor = self.connection.execute(query, (group_name,))
        rows = cursor.fetchall()

        if (not rows):
            return rows

        query = 'SELECT persons.stage_name FROM in_group JOIN persons WHERE in_group.id_group = ? AND in_group.id_person = persons.id_person'
        cursor = self.connection.execute(query, (rows[0][0],))
        rows = cursor.fetchall()
        return rows


    def get_group(self, performer_name):
        """
        Gets the group the performer's is in

        :param performer_name: The name of the performer
        """

        query = 'SELECT start_date, end_date '
        query += 'FROM groups WHERE name = ?'
        cursor = self.connection.execute(query, (performer_name,))
        rows = cursor.fetchall()
        return rows[0]

    def update_song(self, song_id, title, track, year, genre):
        """
        Updates a song

        :param song_id: The song's id
        :param title: The song's title
        :param track: The song's track
        :param year: The song's year
        :param genre: The song's genre
        """

        query = 'UPDATE rolas SET title = ?, track = ?, year = ?, genre = ? '
        query += 'WHERE id_rola = ?'
        self.connection.execute(query, (title, track, year, genre, song_id))
        self.connection.commit()

    def update_performer(self, performer_id, performer_name, new_status):
        """
        Updates a performer

        :param perfomer_id: The performer's id
        :param perfomer_name: The performer's name
        :param new_status: The performers status
        """

        query = 'UPDATE performers SET name = ?, id_type = ? '
        query += 'WHERE id_performer = ?'
        self.connection.execute(query, (performer_name, new_status, performer_id))
        self.connection.commit()

    def update_album(self, album_id, album_name, album_year):
        """
        Updates an album

        :param album_id: The album's id
        :param album_name: The album's name
        :param album_year: The album's year
        """

        query = 'UPDATE albums SET name = ?, year = ? '
        query += 'WHERE id_album = ?'
        self.connection.execute(query, (album_name, album_year, album_id))
        self.connection.commit()

    def insert_person(self, performer_name):
        """
        Inserts a person in the database

        :param performer_name: The performer's name
        """

        query = 'INSERT INTO persons (stage_name) VALUES (?)'
        self.connection.execute(query, (performer_name,))
        self.connection.commit()

    def update_person(self, stage_name, real_name, birth_date, death_date):
        """
        Updates a person

        :param stage_name: The person's stage name
        :param real_name: The person's real name
        :param birth_date: The person's birth date
        :param death_date: The person's death date
        """

        query = 'UPDATE persons SET stage_name = ?, real_name = ?, birth_date = ?, '
        query += 'death_date = ? '
        query += 'WHERE stage_name = ?'
        self.connection.execute(query, (stage_name, real_name, birth_date, death_date, stage_name))
        self.connection.commit()

    def insert_group(self, group_name):
        """
        Inserts a group in the database

        :param group_name: The group's name
        """

        query = 'INSERT INTO groups (name) VALUES (?)'
        self.connection.execute(query, (group_name,))
        self.connection.commit()

    def update_group(self, group_name, start_date, end_date):
        """
        Updates a group

        :param group_name: The group's name
        :param start_date: The group's start date
        :param end_date: The group's end date
        """

        query = 'UPDATE groups SET name = ?, start_date = ?, end_date = ? '
        query += 'WHERE name = ?'
        self.connection.execute(query, (group_name, start_date, end_date, group_name))
        self.connection.commit()

    def add_person_to_group(self, person_name, id_group):
        """
        Adds a person to a group

        :param person_name: The person's name
        :param id_group: The group's id
        """

        query = 'SELECT id_person FROM persons WHERE stage_name = ?'
        cursor = self.connection.execute(query, (person_name,))
        rows = cursor.fetchall()

        id_person = rows[0][0]

        query = 'INSERT INTO in_group (id_person, id_group) VALUES (?, ?)'
        self.connection.execute(query, (id_person, id_group))
        self.connection.commit()

    def send_query(self, query):
        """
        Sends a query to the database

        :param query: The query to send
        :return: The query's result
        """

        cursor = self.connection.execute(query)
        return cursor.fetchall()
