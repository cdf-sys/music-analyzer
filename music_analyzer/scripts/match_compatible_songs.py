from music_analyzer.scripts.key_cam_comm_swapper import swap_keys_and_camelots
from src.tags.id3_handler import find_song_id3_tags, find_songs_by_id3_tags
from src.bpm_key_camelot.camelot_and_key import camelot_check, cam_or_key_to_adjacent_camelots
from src.bpm_key_camelot.bpm_and_key import key_check

keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]


# TODO: modify this function to work with +/- 1 and +/- 2 semitone shifts
# finds songs which would be compatible with the given audio file via camelot neighbors and common BPM
# inputs (2): filename (location of the audio file to be checked), directory (location of the audio files to be checked)
# outputs (1): a list of songs, as well as the tags and values derived from find_songs_by_id3_tags
def find_next_song(filename, directory):
    song_data = find_song_id3_tags(filename, ["TKEY", "TBPM"])  # find the original song's key and BPM
    cam_data = song_data[0].text[0]
    if camelot_check(cam_data) == -1:
        if key_check(cam_data, keys) == -1:
            return None  # the key tag value is not a key or camelot
        else:
            swap_keys_and_camelots(directory)  # if it is a key, convert it to a camelot
    compat_tags = ["TBPM", "TKEY"]
    compat_bpm = list(range(int(int(song_data[1].text[0]) * 0.97) - 1, int(int(song_data[1].text[0]) * 1.03)))
    compat_bpm_str = []  # all key values within 3% of the original song are compatible with it
    for bpm_val in compat_bpm:
        compat_bpm_str.append(str(bpm_val))  # convert BPM values into strings for analysis against other BPM strings
    compat_bpm_cam = [compat_bpm_str, cam_or_key_to_adjacent_camelots(cam_data)]  # generate adjacent camelot values
    return find_songs_by_id3_tags(directory, compat_tags, compat_bpm_cam)
