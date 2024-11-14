from src.bpm_key_camelot.bpm_and_key import key_check
import re

key_fifths = ["G#/Ab", "D#/Eb", "A#/Bb", "F", "C", "G", "D", "A", "E", "B", "F#/Gb", "C#/Db"]


# returns a list separating the number and letter of the camelot if valid, and a negative value otherwise
# inputs (1): input_camelot (camelot to be checked)
# outputs (1): input_camelot separated into a list containing number and letter if valid, otherwise -1
def camelot_check(input_camelot):
    alphanum = re.split("(\\d+)", input_camelot)  # separates the letter and number of the camelot
    if len(alphanum) < 2:
        return -1  # invalid input
    elif int(alphanum[1]) > 12 or int(alphanum[1]) < 1 or (alphanum[2] != 'A' and alphanum[2] != 'B'):
        return -1  # invalid input
    else:
        return alphanum  # valid camelot value


# converts an input key into the camelot scale
# inputs (1): input_key (key to be converted into a camelot value)
# outputs (1): input_key as a camelot, or None if the input is invalid
def key_to_camelot(input_key):
    circular_key = key_check(input_key.strip("m"), key_fifths)
    if circular_key == -1:
        return None  # invalid key input
    else:
        if input_key.find("m") != -1:
            return str(circular_key + 1) + "A"  # return minor scale camelot
        elif (circular_key + 4) % 12 != 0:
            return str((circular_key + 4) % 12) + "B"  # return major scale camelot
        else:
            return str(circular_key + 4) + "B"  # return major scale camelot; ensure a value of 12 rather than 0


# converts an input camelot into a key
# inputs (1): input_camelot (camelot to be converted into a key value)
# outputs (1): input_camelot as a key, or None if the input is invalid
def camelot_to_key(input_camelot):
    alphanum = camelot_check(input_camelot)
    if alphanum == -1:
        return None  # invalid camelot input
    elif alphanum[2] == 'A':
        return key_fifths[int(alphanum[1]) - 1] + "m"  # return minor scale key
    elif alphanum[2] == 'B' and (int(alphanum[1]) - 4) % 12 != 0:
        return key_fifths[(int(alphanum[1]) - 4) % 12]  # return major scale key
    else:
        return key_fifths[int(alphanum[1]) - 4]  # return major scale key; ensure index is within bounds of key_fifths


# outputs the camelots compatible with a given key or camelot value
# inputs (1): input_camelot (camelot or key to be examined for compatible camelot values)
# outputs (1): list of camelots which can are compatible with the input key or camelot, or None with an invalid input
def cam_or_key_to_adjacent_camelots(input_camelot):
    alphanum = camelot_check(input_camelot)
    if alphanum == -1:
        temp_key = key_to_camelot(input_camelot)  # if the input is a valid key, convert it to camelot
        if temp_key is not None:
            alphanum = camelot_check(temp_key)
        else:
            return None  # input isn't a valid camelot or key
    if alphanum[1] == "1":  # ensure that 1 is adjacent to 12 rather than 0
        return ["".join(alphanum), alphanum[1] + alphanum[2].translate({ord('A'): 'B', ord('B'): 'A'}),
                str(int(alphanum[1]) + 1) + alphanum[2], "12" + alphanum[2]]
    elif alphanum[1] == "11":  # ensure that 11 is adjacent to 12 rather than 0
        return ["".join(alphanum), alphanum[1] + alphanum[2].translate({ord('A'): 'B', ord('B'): 'A'}),
                "12" + alphanum[2], str(int(alphanum[1]) - 1) + alphanum[2]]
    else:  # general case scenario
        return ["".join(alphanum), alphanum[1] + alphanum[2].translate({ord('A'): 'B', ord('B'): 'A'}),
                str((int(alphanum[1]) + 1) % 12) + alphanum[2],
                str((int(alphanum[1]) - 1) % 12) + alphanum[2]]
