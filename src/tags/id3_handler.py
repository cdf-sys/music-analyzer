# information about mutagen's ID3 tag frames can be found here:
# https://mutagen-specs.readthedocs.io/en/latest/id3/id3v2.4.0-frames.html
from mutagen.id3 import ID3, ID3NoHeaderError, COMM, TKEY
from mutagen import MutagenError
import os


# ensures that a song exists given a file name
# inputs (1): filename (location of the audio file to be checked)
# outputs (1): an ID3 object representing the file at filename if it exists and has ID3 tags, otherwise None
def find_song(filename):
    try:
        audio = ID3(filename)
    except (FileNotFoundError, ID3NoHeaderError, MutagenError):
        return None  # the file does not exist, does not have ID3 tags, or is a file type incompatible with ID3
    return audio


# find the ID3 tag values of a song coinciding with a list of desired tag frames
# inputs (2): filename (location of the audio file to be checked), tags (list of ID3 tag frames to return the values of)
# outputs (1): a list of values coinciding with ID3 tag frame values, or None if provided an invalid file
def find_song_id3_tags(filename, tags):
    song = find_song(filename)
    if song is None:
        return None  # the file does not exist, does not have ID3 tags, or is a file type incompatible with ID3
    desired_tags = []
    for tag in tags:
        try:
            desired_tags.append(song[tag])  # add the ID3 tag value according to the tag frame to desired_tags
        except KeyError:
            desired_tags.append(None)  # the ID3 tag frame does not exist
    return desired_tags


# get a list of songs according to lists of desired ID3 tags and desired tag values
# inputs (3): directory (location of the audio files to be checked), tags (list of ID3 tag frames to check), vals
#             (list of desired values for each tag in tags)
# outputs (1): a list of songs with desired tags and respective values appended to the end
def find_songs_by_id3_tags(directory, tags, vals):
    songs = []
    for files in os.walk(directory):
        for file in files[2]:  # find the real value of each tag frame for each file in the directory
            real_vals = find_song_id3_tags(os.path.join(files[0], file), tags)
            songs_by_tag = [file]
            for i in range(0, len(tags)):  # check each tag individually
                for target_val in vals[i]:  # check the list in vals that coincides with the respective tag
                    target_val = str(target_val)
                    if target_val in real_vals:
                        songs_by_tag.append(tags[i])     # check vals for the real tag value, and append the tag and
                        songs_by_tag.append(target_val)  # the real value of the tag if it matches a value in vals
                    else:
                        continue
            if len(songs_by_tag) == 1 + 2 * len(tags):
                songs.append(songs_by_tag)  # append the song to songs if all tags have been appended to songs_by_tag
    return songs


# swap the key and comment of a provided song
# inputs (1): filename (location of the audio file to be checked)
# outputs (1): the song after having swapped key and comment, or None if provided an invalid file
def swap_song_key_and_comment(filename):
    song = find_song(filename)
    if song is None:
        return None  # the file does not exist, does not have ID3 tags, or is a file type incompatible with ID3
    else:
        try:
            temp_tag1 = song["TKEY"].text[0]  # temp_tag1 = previous key value
        except KeyError:
            temp_tag1 = ""
            song.add(TKEY(encoding=3, text=temp_tag1))
            song.save()  # create an empty key tag if it doesn't exist
        try:
            temp_tag2 = song["COMM:ID3v1 Comment:eng"].text[0]  # temp_tag2 = previous comment value
        except KeyError:
            temp_tag2 = ""
            song.add(COMM(desc='ID3v1 Comment', lang='eng', text=temp_tag2))
            song.save()  # create an empty comment tag if it doesn't exist
        song["TKEY"].text[0] = temp_tag2
        song["COMM:ID3v1 Comment:eng"].text[0] = temp_tag1
        song.save()  # swap the tags and save the song metadata
        return song
