from bpm_and_key import key_check
import re

key_fifths = ["G#/Ab", "D#/Eb", "A#/Bb", "F", "C", "G", "D", "A", "E", "B", "F#/Gb", "C#/Db"]


def key_to_camelot(input_key):
    circular_key = key_check(input_key.strip("m"), key_fifths)
    if circular_key == -1:
        return None
    else:
        if input_key.find("m") != -1:
            return str(circular_key + 1) + "A"
        elif (circular_key + 4) % 12 != 0:
            return str((circular_key + 4) % 12) + "B"
        else:
            return str(circular_key + 4) + "B"


def key_to_adjacent_camelots(input_key):
    camelot_base = key_to_camelot(input_key)
    if camelot_base is None:
        return None
    else:
        camelots = [camelot_base]
        alphanum = re.split("(\\d+)", camelot_base)
        camelots.append(alphanum[1] + "" + alphanum[2].translate({ord('A'):'B', ord('B'):'A'}))
        camelots.append(str((int(alphanum[1]) + 1) % 12) + "" + alphanum[2])
        camelots.append(str((int(alphanum[1]) - 1) % 12) + "" + alphanum[2])
        return camelots
