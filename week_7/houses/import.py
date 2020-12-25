# Houses

# Libs
from cs50 import SQL
from csv import reader
from sys import argv

# Check input arguments
if (len(argv) < 2 or len(argv) >= 3):
    print("usage error, import.py characters.csv")
    exit()

# Open the database
db = SQL("sqlite:///students.db")

with open(argv[1]) as characters_file:
    characters = reader(characters_file)
    for character in characters:

        # Check Header (if not header continue)
        if character[0] != 'name':

            # Auto split
            full_name = character[0].split()

            # Check
            # If the Middle is available
            if (len(full_name) > 2):
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                           full_name[0], full_name[1], full_name[2], character[1], character[2])

            # If only the name and family is available
            else:
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                           full_name[0], None, full_name[1], character[1], character[2])