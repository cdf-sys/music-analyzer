import math
import re

keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]


# returns a positive value if the input key is within the given key set, and a negative value otherwise
# inputs (2): input_key (key to be checked), key_set (list of key values to be checked against)
# outputs (1): the index of input_key within key_set if it is found there, otherwise -1
def key_check(input_key, key_set):
    if input_key is None or ((input_key.find("A") != -1 or
                              input_key.find("B") != -1) and bool(re.search(r'\d', input_key))):
        return -1  # the input is None or in camelot form
    else:
        temp_key = input_key
        if temp_key.find("#") != -1 or temp_key.find("b") != -1:  # the input is flat/sharp
            for key in key_set:
                if temp_key in key:
                    temp_key = input_key  # ensure the correct key will be found if only provided a flat or sharp key
        count = 0
        for key in key_set:
            if key == temp_key:
                return count  # return the index of the correct key within key_set
            count += 1
    return -1


# calculates the nearest key upon changing the BPM of a song
# inputs (3): prev_bpm (BPM before change), key (key before change), curr_bpm (BPM for the song to be changed to)
# outputs (2): nearest key after the BPM change, margin of key change calculation error, or None with invalid inputs
def key_after_bpm_shift(prev_bpm, curr_bpm, key):
    curr_key = key_check(key.strip("m"), keys)  # remove the mode before checking the key
    if curr_key == -1 or prev_bpm < 0 or curr_bpm < 0:
        return None, None  # invalid key or BPM value
    elif prev_bpm == curr_bpm:
        return key, 0  # no BPM change
    else:
        new_key_val = (curr_key + math.log2(prev_bpm / curr_bpm) * 12) % 12
        new_key_est = round(new_key_val)  # value used to determine key and error margin
        return keys[new_key_est], abs(new_key_val - new_key_est)


# calculates the BPM upon changing the key of a song
# inputs (3): prev_key (key before change), bpm (BPM before change), curr_key (key for the song to be changed into)
# outputs (1): BPM after the key change, or -1 if inputs are invalid
def bpm_after_key_shift(bpm, prev_key, curr_key):
    modeless_prev_key = prev_key.strip("m")
    modeless_curr_key = curr_key.strip("m")
    prev_key_valid = key_check(modeless_prev_key, keys)
    curr_key_valid = key_check(modeless_curr_key, keys)
    if prev_key_valid == -1 or curr_key_valid == -1 or bpm < 0 or (
            (modeless_prev_key == prev_key) != (modeless_curr_key == curr_key)):
        return -1  # invalid key or BPM values, or key modes do not match
    elif prev_key_valid == curr_key_valid:
        return bpm  # no key change
    else:
        return bpm * 2 ** ((curr_key_valid - prev_key_valid) / 12)


# calculates the BPMs needed to obtain each of the 12 keys if increasing or decreasing the BPM of a song
# inputs (3): bpm, key (BPM and key before shifting the song), upward (BPM increase if true, otherwise decrease)
# outputs (1): a list of 12 BPMs in order of the key list as checked against by key_check, or None with invalid inputs
def all_bpm_after_key_shift(bpm, key, upward):
    curr_key = key_check(key.strip("m"), keys)
    if curr_key == -1:  # invalid key
        return None
    else:
        bpm_list = []
        for i in range(0, 12):  # iterate once for each key
            if upward:
                key_factor = curr_key - i
                if curr_key - i < 0:
                    key_factor += 12  # ensure that the BPM will be higher than the original
                bpm_list.append(bpm * 2 ** ((12 - key_factor) / 12))
            else:
                key_factor = i - curr_key
                if i - curr_key > 0:
                    key_factor -= 12  # ensure that the BPM will be lower than the original
                bpm_list.append(bpm * 2 ** (-(12 + key_factor) / 12))
        return bpm_list
