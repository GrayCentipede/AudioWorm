import sqlite3

class Manager(object):

    connection = None

    def __init__(self):
        self.connection = sqlite3.connect('./sql/audioworm.db')

    def get_all_songs(self):
        query = 'SELECT rolas.title, performers.name, albums.name, rolas.track, rolas.year, rolas.genre,'
        query += 'rolas.path, performers.id_type FROM rolas JOIN performers JOIN albums '
        query += 'WHERE rolas.id_performer = performers.id_performer AND rolas.id_album = albums.id_album '
        query += 'ORDER BY performers.name'
        cursor = self.connection.execute(query)
        return cursor.fetchall()
