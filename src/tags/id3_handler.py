from mutagen.id3 import ID3, ID3NoHeaderError, COMM, TKEY
from mutagen import MutagenError
import os


def find_song(filename):
    try:
        audio = ID3(filename)
    except (FileNotFoundError, ID3NoHeaderError, MutagenError):
        return None
    return audio


def find_song_id3_tags(filename, tags):
    song = find_song(filename)
    if song is None:
        return None
    desired_tags = []
    for tag in tags:
        try:
            desired_tags.append(song[tag])
        except KeyError:
            desired_tags.append(None)
    return desired_tags


def find_songs_by_id3_tags(directory, tags, vals):
    songs = []
    for files in os.walk(directory):
        for file in files[2]:
            real_vals = find_song_id3_tags(os.path.join(files[0], file), tags)
            songs_by_tag = [file]
            for i in range(0, len(tags)):
                for target_val in vals[i]:
                    target_val = str(target_val)
                    if target_val in real_vals:
                        songs_by_tag.append(tags[i])
                        songs_by_tag.append(target_val)
                    else:
                        continue
            if len(songs_by_tag) == 1 + 2 * len(tags):
                songs.append(songs_by_tag)
    return songs


def swap_song_key_and_comment(filename):
    song = find_song(filename)
    if song is None:
        return None
    else:
        try:
            temp_tag1 = song["TKEY"].text[0]
        except KeyError:
            temp_tag1 = ""
            song.add(TKEY(encoding=3, text=temp_tag1))
            song.save()
        try:
            temp_tag2 = song["COMM:ID3v1 Comment:eng"].text[0]
        except KeyError:
            temp_tag2 = ""
            song.add(COMM(desc='ID3v1 Comment', lang='eng', text=temp_tag2))
            song.save()
        song["TKEY"].text[0] = temp_tag2
        song["COMM:ID3v1 Comment:eng"].text[0] = temp_tag1
        song.save()
        return song
