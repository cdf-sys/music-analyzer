from music_analyzer.scripts.key_cam_comm_swapper import swap_keys_and_comments, swap_keys_and_camelots

if __name__ == "__main__":
    while True:
        directory = input("Please enter a file directory containing music files: ").replace("/", "\\")
        cam_or_comm = input("Type A to swap comment and key metadata, or B to swap key metadata from camelot to key "
                            "or vice versa: ")
        while cam_or_comm != "A" and cam_or_comm != "B":
            cam_or_comm = input("Type A to swap comment and key metadata, or B to swap key metadata from camelot to "
                                "key or vice versa: ")
        if cam_or_comm == "A":
            swap_keys_and_comments(directory)
            print("Successfully swapped keys and comments!\n")
        else:
            swap_keys_and_camelots(directory)
            print("Successfully swapped keys and camelots!\n")
