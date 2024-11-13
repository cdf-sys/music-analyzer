from mutagen.id3 import ID3, ID3NoHeaderError, COMM
from mutagen import MutagenError
import os


def find_song(filename):
    try:
        audio = ID3(filename)
    except (FileNotFoundError, ID3NoHeaderError, MutagenError):
        print("yo")
        return None
    return audio


def find_song_id3_tags(filename, tag):
    song = find_song(filename)
    if song is None:
        return None
    try:
        return song[tag]
    except KeyError:
        return None


def find_songs_by_id3_tag(directory, tag, tag_value):
    songs = []
    for files in os.walk(directory):
        for file in files[2]:
            iter_tag = find_song_id3_tags(os.path.join(files[0], file), tag)
            if iter_tag is not None:
                if iter_tag == tag_value:
                    songs.append([file, tag_value])
    return songs


def swap_song_id3_tags(filename, first_tag, second_tag):
    song = find_song(filename)
    if song is None:
        return None
    else:
        try:
            temp_tag1 = song[first_tag].text[0]
        except KeyError:
            temp_tag1 = ""
            if first_tag.find("eng") != -1:
                song.add(COMM(encoding=3, lang='eng', text=temp_tag1))
                song.save()
                song[COMM] = COMM(encoding=3, lang='eng', text=temp_tag1)
            else:
                song.add(first_tag)
                song[first_tag] = first_tag(encoding=3, text=temp_tag1)
            song.save()
        try:
            temp_tag2 = song[second_tag].text[0]
        except KeyError:
            temp_tag2 = ""
            if second_tag.find("eng") != -1:
                song.add(COMM(encoding=3, lang='eng', text=temp_tag2))
                song.save()
                song[COMM] = COMM(encoding=3, lang='eng', text=temp_tag2)
            else:
                song.add(second_tag)
                song[second_tag] = second_tag(encoding=3, text=temp_tag2)
            song.save()
        song[first_tag].text[0] = temp_tag2
        song[second_tag].text[0] = temp_tag1
        song.save()
        return song
