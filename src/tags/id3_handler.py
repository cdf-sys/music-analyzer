from mutagen.id3 import ID3, ID3NoHeaderError
import os


def find_song(filename):
    try:
        audio = ID3(filename)
    except FileNotFoundError:
        return None
    except ID3NoHeaderError:
        return None
    return audio


def find_song_id3_tags(filename, tag):
    song = find_song(filename)
    if song is None or song[tag] is None:
        return None
    else:
        return song[tag]


def find_songs_by_id3_tag(directory, tag, tag_value):
    songs = []
    for files in os.walk(directory):
        for file in files[2]:
            iter_tag = find_song_id3_tags(os.path.join(files[0], file), tag)
            if iter_tag is not None:
                if iter_tag == tag_value:
                    songs.append(file)
    return songs


def swap_song_id3_tags(filename, first_tag, second_tag):
    song = find_song(filename)
    if song is None or (song[first_tag] is None and song[second_tag] is None):
        return None
    else:
        temp_tag = song[first_tag].text[0]
        song[first_tag].text[0] = song[second_tag].text[0]
        song[second_tag].text[0] = temp_tag
        song.save()
        return song
