# Imports
import pickle
import song_class


# Constants
DATABASE_FP = "data/song_features.txt"

# Variables
database = {}


def retrieve_database(filepath=DATABASE_FP):
    """
    Retrieves database dictionary from filepath.
    :param filepath: filepath of database
    :return: dictionary of database
    """
    with open(filepath, "rb") as f:
        db = pickle.load(f)
    return db


def write_database(filepath=DATABASE_FP):
    """
    Writes database dictionary to filepath.
    :param filepath: filepath of database
    """
    with open(filepath, "wb") as f:
        pickle.dump(database, f)


def add_song(features, name, artist):
    """
    Adds song to database.
    :param features: List of feature tuples.
    :param name: String
    :param artist: String
    """
    song = song_class.Song(name, artist)
    for feat in features:
        if feat[0] in database:
            database[feat[0]].append((song, feat[1]))
        else:
            database[feat[0]] = [(song, feat[1])]


def get_songs_from_db():
    """
    Retrieves song set from database.
    :return: List of songs
    """
    songs = set()
    for feature in database.keys():
        for song in database[feature]:
            if song[0] not in songs:
                songs.add(song[0])
    return songs


def retrieve_song_features(song_name):
    feats = set()
    for feature in database.keys():
        for song in database[feature]:
            if song[0].name == song_name:
                if feature not in feats:
                    feats.add(feature)
                break
    return feats


def display_songs():
    """
    Displays songs and artists from database.
    """
    for song in list(get_songs_from_db()):
        print(song.name, "by", song.artist)


def get_song_object(song_name):
    song_feature = list(retrieve_song_features(song_name))[0]
    print(song_feature)
    return [i[0]
            for i in database[song_feature]
            if i[0].name == song_name][0]


def remove_song(song):
    for feature in database.keys():
        song_time_tup = database[feature]

        zipped = zip(*song_time_tup)
        combined = list(zipped)
        songs = list(combined[0])
        times = list(combined[1])

        while song in songs:
            ind = songs.index(song)
            songs.remove(song)
            times.remove(times[ind])

        updated = list(zip(songs, times))
        database[feature] = updated

    i = database.copy()
    for k, v in i.items():
        if v == []:
            del database[k]


def clear_database(password):
    """
    Clears database with two confirms. Enter 'y' to confirm when prompted.
    Remember to write to database afterwards.
    :param password: String ("yes i am sure")
    """
    if password.lower() == "yes i am sure":
        if input("Are you very sure?").lower() == "y":
            global database
            database = {}


def initialize():
    """Automatically retrieves database."""
    global database
    database = retrieve_database()

initialize()

