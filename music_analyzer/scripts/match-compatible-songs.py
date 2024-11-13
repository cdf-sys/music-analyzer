from music_analyzer.scripts.key_cam_comm_swapper import swap_keys_and_camelots
from src.tags.id3_handler import find_song_id3_tags, find_songs_by_id3_tag
from src.bpm_key_camelot.camelot_and_key import camelot_check, cam_or_key_to_adjacent_camelots
from src.bpm_key_camelot.bpm_and_key import key_check
import os

keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]


def find_next_song(filename, directory):
    song_cam = find_song_id3_tags(filename, "TKEY").text[0]
    if camelot_check(song_cam) == -1:
        if key_check(song_cam, keys) == -1:
            return None
        else:
            swap_keys_and_camelots(directory)
    song_bpm = find_song_id3_tags(filename, "TBPM").text[0]
    tracks = []
    tracks_temp = []
    compat = cam_or_key_to_adjacent_camelots(song_cam)
    bpm_sync = list(range(int(int(song_bpm) * 0.97) - 1, int(int(song_bpm) * 1.03)))
    for cams in compat:
        cam_list = find_songs_by_id3_tag(directory, "TKEY", cams)
        for tunes in cam_list:
            tracks_temp.append(tunes)
    for track in tracks_temp:
        iter_bpm = find_song_id3_tags(os.path.join(directory, track[0]), "TBPM")
        if iter_bpm is not None:
            if bpm_sync[0] <= int(iter_bpm.text[0]) <= bpm_sync[len(bpm_sync) - 1]:
                tracks.append([track[0], iter_bpm.text[0], track[1]])
    return tracks


if __name__ == "__main__":
    print(find_next_song("E:\\tunes-test\\$uicideboy$ - 2nd Hand.mp3", "E:\\tunes-test\\"))