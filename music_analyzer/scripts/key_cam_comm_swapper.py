from src.bpm_key_camelot.bpm_and_key import key_check
from src.bpm_key_camelot.camelot_and_key import camelot_check, camelot_to_key, key_to_camelot
from src.tags.id3_handler import find_song_id3_tags, swap_song_key_and_comment
from mutagen.id3 import ID3
import os

keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]


def comment_key_check(filename):
    key_data = find_song_id3_tags(filename, ["TKEY", "COMM::eng"])
    if key_data[0] is None and key_data[1] is None:
        return -1, None
    else:
        for i in range(0, 1):
            if key_data[i] is not None:
                if key_check(str(key_data[i].text[0]).strip("m"), keys) != -1:
                    return 0 + 2 * i, key_data[i].text[0]
                elif camelot_check(str(key_data[i])) != -1:
                    return 1 + 2 * i, key_data[i].text[0]
        return -1, None


def swap_keys_and_comments(directory):
    for files in os.walk(directory):
        for file in files[2]:
            file_path = os.path.join(files[0], file)
            if comment_key_check(file_path)[0] != -1:
                swap_song_key_and_comment(file_path)
    return None


def swap_keys_and_camelots(directory):
    for files in os.walk(directory):
        for file in files[2]:
            file_path = os.path.join(files[0], file)
            vals = comment_key_check(file_path)
            if vals[0] > -1:
                song = ID3(file_path)
                if vals[0] == 0:
                    song["TKEY"].text[0] = str(key_to_camelot(vals[1]))
                elif vals[0] == 1:
                    song["TKEY"].text[0] = str(camelot_to_key(vals[1]))
                song.save()
    return None
