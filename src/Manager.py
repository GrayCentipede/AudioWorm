import sqlite3

class Manager(object):

    connection = None

    def __init__(self):
        self.connection = sqlite3.connect('./sql/audioworm.db')

    def get_all_songs(self):
        query = 'SELECT rolas.title, performers.name, albums.name, rolas.track, rolas.year, rolas.genre,'
        query += 'rolas.path, rolas.id_performer, performers.id_type, rolas.id_album, rolas.id_rola '
        query += 'FROM rolas JOIN performers JOIN albums '
        query += 'WHERE rolas.id_performer = performers.id_performer AND rolas.id_album = albums.id_album '
        query += 'ORDER BY performers.name'
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def get_person(self, performer_name):
        query = 'SELECT real_name, birth_date, death_date '
        query += 'FROM persons WHERE stage_name = ?'
        cursor = self.connection.execute(query, (performer_name,))
        rows = cursor.fetchall()
        return rows[0]

    def update_song(self, song_id, title, track, year, genre):
        query = 'UPDATE rolas SET title = ?, track = ?, year = ?, genre = ? '
        query += 'WHERE id_rola = ?'
        self.connection.execute(query, (title, track, year, genre, song_id))
        self.connection.commit()

    def update_performer(self, performer_id, performer_name, new_status):
        query = 'UPDATE performers SET name = ?, id_type = ? '
        query += 'WHERE id_performer = ?'
        self.connection.execute(query, (performer_name, new_status, performer_id))
        self.connection.commit()

    def update_album(self, album_id, album_name, album_year):
        query = 'UPDATE albums SET name = ?, year = ? '
        query += 'WHERE id_album = ?'
        self.connection.execute(query, (album_name, album_year, album_id))
        self.connection.commit()

    def insert_person(self, performer_name):
        query = 'INSERT INTO persons (stage_name) VALUES (?)'
        self.connection.execute(query, (performer_name,))
        self.connection.commit()

    def update_person(self, stage_name, real_name, birth_date, death_date):
        query = 'UPDATE persons SET stage_name = ?, real_name = ?, birth_date = ?, '
        query += 'death_date = ? '
        query += 'WHERE persons.stage_name = ?'
        self.connection.execute(query, (stage_name, real_name, birth_date, death_date, stage_name))
        self.connection.commit()

    def update_group(self, group_name, start_date, end_date):
        pass
