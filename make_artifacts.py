#!/usr/bin/env python

import pprint
import glob

python_filenames = []


def process_file(filename):
    f = open(filename)

    unscii_bytes = {}
    unscii_transposed_bytes = {}

    for line in f:
        unicode, hex = line.split(":")
        hex = hex.rstrip()
        unicode_entry = int(unicode, 16)
        hex_bytes = []
        byte_count = 0
        while len(hex) > 0:
            byte_count += 1
            byte = hex[0:2]
            hex = hex[2:]
            hex_bytes.append(int(byte,16))
        unscii_bytes[unicode_entry] = hex_bytes

        transposed_bytes = [0 for _ in range(byte_count)]
        for i in range(len(hex_bytes)):
            hex_line = hex_bytes[i]
            for j in range(8):
                bit = hex_line & (1 << (7 -j))
                if bit:
                    transposed_bytes[j] += 1 << i
        unscii_transposed_bytes[unicode_entry] = transposed_bytes
    just_filename = filename.split("/")[-1]
    just_filename_without_extension = just_filename[0:-4]

    python_friendly_name = just_filename_without_extension.replace("-", "_")

    unscii_bytes_file = open("./unscii/raw_unscii/%s.py" % python_friendly_name, "w")
    unscii_bytes_file.write("# File generate by unscii.py. Not intended to be read or modified by humans.\n\n")
    unscii_bytes_file.write("%s_bytes = " % python_friendly_name)
    unscii_bytes_file.write(pprint.pformat(unscii_bytes))

    transposed_python_friendly_name = python_friendly_name + "_transposed"
    
    unscii_bytes_file = open("./unscii/raw_unscii/%s.py" % transposed_python_friendly_name, "w")
    unscii_bytes_file.write("# File generate by unscii.py. Not intended to be read or modified by humans.\n\n")
    unscii_bytes_file.write("%s_bytes = " % transposed_python_friendly_name)
    unscii_bytes_file.write(pprint.pformat(unscii_transposed_bytes))

    return [python_friendly_name, transposed_python_friendly_name]

def process_files():
    for filename in glob.glob("./hexfiles/*.hex"):
        next_python_filenames = process_file(filename)
        python_filenames.extend(next_python_filenames)

    raw_unscii_init_file = open("./unscii/raw_unscii/__init__.py", "w")
    raw_unscii_init_file.write("# File generate by unscii.py. Not intended to be read or modified by humans.\n\n")
    raw_unscii_init_file.write("raw_unscii_modules = %s" % pprint.pformat(python_filenames))
    
if __name__ == "__main__":
    process_files()
