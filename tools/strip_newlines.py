"""
Strips newlines from files and replaces them with spaces.
Good to run this on .sh files created on Windows,
as newlines seem to confuse Ubuntu when sourcing .sh files in the console.

This is not really needed anymore, as the project is now using python-dotenv to handle
environment variables.
"""

import sys

def main(argv):
    if len(argv) > 1:
        with open(argv[1], "r") as file:
            read = file.read()
            stripped_string = read.replace("\n", " ")
            with open(argv[1], "w") as file_out:
                file_out.write(stripped_string)
    else:
        print("Please supply a file name.")

if __name__ == "__main__":
    main(sys.argv)
