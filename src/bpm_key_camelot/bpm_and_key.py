import math

keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]


def key_check(input_key, key_set):
    input_key_fix = key_correction(input_key, key_set)
    count = 0
    for key in key_set:
        if key == input_key_fix:
            return count
        count += 1
    return -1


def key_correction(input_key, key_set):
    if input_key.find("#") != -1 or input_key.find("b") != -1:
        for key in key_set:
            if input_key in key:
                return key
    return input_key


def key_after_bpm_shift(prev_bpm, curr_bpm, key):
    curr_key = key_check(key.strip("m"), keys)
    if curr_key == -1 or prev_bpm < 0 or curr_bpm < 0:
        return None
    elif prev_bpm == curr_bpm:
        return key
    else:
        new_key_val = (curr_key + math.log2(prev_bpm / curr_bpm) * 12) % 12
        new_key_est = round(new_key_val)
        return keys[new_key_est], abs(new_key_val - new_key_est)


def bpm_after_key_shift(bpm, prev_key, curr_key):
    modeless_prev_key = prev_key.strip("m")
    modeless_curr_key = curr_key.strip("m")
    prev_key_valid = key_check(modeless_prev_key, keys)
    curr_key_valid = key_check(modeless_curr_key, keys)
    if prev_key_valid == -1 or curr_key_valid == -1 or bpm < 0 or (
            (prev_key.strip("m") == prev_key) != (curr_key.strip("m") == curr_key)):
        return -1
    elif prev_key_valid == curr_key_valid:
        return bpm
    else:
        return bpm * 2 ** ((curr_key_valid - prev_key_valid) / 12)


def bpm_after_octave_shift(bpm, octaves):
    return bpm * 2 ** octaves


def all_bpm_after_key_shift(bpm, key, upward):
    modeless_key = key.strip("m")
    curr_key = key_check(modeless_key, keys)
    if curr_key == -1:
        return None
    else:
        bpm_list = []
        for i in range(0, 12):
            if upward:
                key_factor = curr_key - i
                if curr_key - i < 0:
                    key_factor += 12
                bpm_list.append(bpm * 2 ** ((12 - key_factor) / 12))
            else:
                key_factor = i - curr_key
                if i - curr_key > 0:
                    key_factor -= 12
                bpm_list.append(bpm * 2 ** (-(12 + key_factor) / 12))
        return bpm_list
