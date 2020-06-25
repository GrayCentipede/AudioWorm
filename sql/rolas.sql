CREATE TABLE types (
    id_type       INTEGER PRIMARY KEY,
    description   TEXT
);

INSERT INTO types VALUES(0,'Person');
INSERT INTO types VALUES(1,'Group');
INSERT INTO types VALUES(2,'Unknown');

CREATE TABLE performers (
    id_performer  INTEGER PRIMARY KEY,
    id_type       INTEGER,
    name          TEXT,
    FOREIGN KEY   (id_type) REFERENCES types(id_type)
);

CREATE TABLE people (
    id_people     INTEGER PRIMARY KEY,
    stage_name    TEXT,
    real_name     TEXT,
    birth_date    TEXT,
    death_date    TEXT
);

CREATE TABLE groups (
    id_group      INTEGER PRIMARY KEY,
    name          TEXT,
    start_date    TEXT,
    end_date      TEXT
);

CREATE TABLE albums (
    id_album      INTEGER PRIMARY KEY,
    path          TEXT,
    name          TEXT,
    year          INTEGER
);

CREATE TABLE songs (
    id_song       INTEGER PRIMARY KEY,
    id_performer  INTEGER,
    id_album      INTEGER,
    path          TEXT,
    title         TEXT,
    track         INTEGER,
    year          INTEGER,
    genre         TEXT,
    FOREIGN KEY   (id_performer) REFERENCES performers(id_performer),
    FOREIGN KEY   (id_album) REFERENCES albums(id_album)
);

CREATE TABLE playlists (
    id_playlist   INTEGER PRIMARY KEY,
    name          TEXT,
    description   TEXT
);

CREATE TABLE in_group (
    id_person     INTEGER,
    id_group      INTEGER,
    PRIMARY KEY   (id_person, id_group),
    FOREIGN KEY   (id_person) REFERENCES people(id_people),
    FOREIGN KEY   (id_group) REFERENCES  groups(id_group)
);

CREATE TABLE in_playlist (
    id_playlist   INTEGER,
    id_song       INTEGER,
    PRIMARY KEY   (id_song, id_song),
    FOREIGN KEY   (id_song) REFERENCES songs(id_song),
    FOREIGN KEY   (id_playlist) REFERENCES playlists(id_playlist)
);
