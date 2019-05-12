"""
Strips newlines from files and replaces them with spaces.
Good to run this on .sh files created on Windows,
as newlines seem to confuse Ubuntu when sourcing .sh files in the console.
"""

import sys

def main(argv):
    if len(argv) > 1:
        with open(argv[1], "r") as file:
            # Some alternative ways of doing this

            # read = file.readlines()
            # print(read)
            # read_string = ("").join(read)
            # stripped_string = read_string.replace("\n", " ")
            # print(stripped_string)

            # stripped_lines = []
            # for line in file:
            #     stripped_lines.append(line.replace("\n", " "))
            # stripped_string = ("").join(stripped_lines)
            # print(stripped_string)

            # lines = file.readlines()
            # stripped_lines = []
            # for line in lines:
            #     stripped_lines.append(line.replace("\n", " "))
            #     # line = line.rstrip()
            # stripped_string = ("").join(stripped_lines)

            read = file.read()
            stripped_string = read.replace("\n", " ")
            with open(argv[1], "w") as file_out:
                file_out.write(stripped_string)
    else:
        print("Please supply a file name.")

if __name__ == "__main__":
    main(sys.argv)
