# Roster

# Libs
from cs50 import SQL
from sys import argv

# Check input arguments
if (len(argv) < 2 or len(argv) >= 3):
    print("usage error, import.py characters.csv")
    exit()

# open the database
db = SQL("sqlite:///students.db")

# Query (Select all except id)
students = db.execute("SELECT first, middle, last, house, birth FROM students WHERE house = (?) ORDER BY last", argv[1])

# Read selectrd datas
for student in students:
    # If the Middle is available
    if student['middle'] != None:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")

    # If only the name and family is available
    else:
        print(f"{student['first']} {student['last']}, born {student['birth']}")