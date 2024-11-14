from src.bpm_key_camelot.bpm_and_key import key_check
from src.bpm_key_camelot.camelot_and_key import camelot_check, camelot_to_key, key_to_camelot
from src.tags.id3_handler import find_song_id3_tags, swap_song_key_and_comment
from mutagen.id3 import ID3
import os

keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]


# check a song to see if a valid key or camelot is in the key or comment field
# inputs (1): filename (location of the audio file to be checked)
# outputs (2): validation index (0 if valid key in key, 1 if valid camelot in key, 2 if valid key in comment, 3 if
#              valid camelot in comment, -1 otherwise), and the key/camelot itself (or None if invalid)
def comment_key_check(filename):
    key_data = find_song_id3_tags(filename, ["TKEY", "COMM::eng"])
    if key_data[0] is None and key_data[1] is None:
        return -1, None  # the song has no value for the key or comment tags
    else:
        for i in range(0, 1):  # iterate through the key tag, then the comment tag
            if key_data[i] is not None:
                if key_check(str(key_data[i].text[0]).strip("m"), keys) != -1:
                    return 0 + 2 * i, key_data[i].text[0]  # valid key; 1 if from TKEY, 3 if from COMM::eng
                elif camelot_check(str(key_data[i])) != -1:
                    return 1 + 2 * i, key_data[i].text[0]  # valid camelot; 2 if from TKEY, 4 if from COMM::eng
        return -1, None  # a valid key or camelot was not found in either tag


# swap the key and comment fields of an entire directory
# inputs (1): directory (location of the audio files to have their key/camelot values swapped)
# outputs (1): None
def swap_keys_and_comments(directory):
    for files in os.walk(directory):
        for file in files[2]:  # iterate through all the files in the directory
            file_path = os.path.join(files[0], file)
            if comment_key_check(file_path)[0] != -1:  # swap the key and comment so long as one of the two tags has a
                swap_song_key_and_comment(file_path)   # valid key or camelot value
    return None


# swap the key tag field of an entire directory from key to camelot, or vice versa
# inputs (1): directory (location of the audio files to have their key/camelot values swapped)
# outputs (1): None
def swap_keys_and_camelots(directory):
    for files in os.walk(directory):
        for file in files[2]:  # iterate through all the files in the directory
            file_path = os.path.join(files[0], file)
            vals = comment_key_check(file_path)  # make sure the key tag field has a valid key or camelot
            if vals[0] > -1:
                song = ID3(file_path)  # find_song can be skipped, since comment_key_check already checks the file
                if vals[0] == 0:  # if the provided tag value is a key, change it into a camelot
                    song["TKEY"].text[0] = str(key_to_camelot(vals[1]))
                elif vals[0] == 1:  # if the provided tag value is a camelot, change it into a key
                    song["TKEY"].text[0] = str(camelot_to_key(vals[1]))
                song.save()  # save changes to each song
    return None
