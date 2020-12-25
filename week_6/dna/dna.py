from csv import reader, DictReader
from sys import argv

# Check input ARGV
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit()

# Read Sequences file (TXT)
with open(argv[2]) as squences_file:
    dna_reader = reader(squences_file)
    for row in dna_reader:
        dna_list = row

# Change List to String
dna_list = dna_list[0]


# Read haeder of CSV file(KEYS)
with open(argv[1]) as people_list:

    # Reas headers and copy to Keys
    HEADERS = next(reader(people_list))
    keys = HEADERS[1:]

    # Create a DICT from prople (create dict_people)
    people = reader(people_list)
    dict_people = []
    for row in people:
        dict_people.append(row)


# Loop for change key and search in TXT file
finded_dna = []
for i, key in enumerate(keys):

    len_key = len(key)
    # Set and reset vars again
    counter = 0
    max_count = 0
    check_first = False

    for i in range(len(dna_list)):
        if (dna_list[i: i + len_key]) == key:

            # In any case, if it is observed once, it makes the value 1
            if (max_count == 0):
                max_count = 1

            # If NOT first detect
            if (dna_list[i - len_key: i] == key):
                # ADD counter
                counter += 1
                # Update Max value
                if counter > max_count:
                    max_count = counter

            # If first detect
            else:
                # Reset Counter
                counter = 0
                # ADD counter
                counter += 1

    # ADD final results to this ARRAY for Comparison
    finded_dna.append(str(max_count))


# Check Result and people's DNA
find = False
for person in dict_people:
    for i in range(len(finded_dna)):

        # IF ==> [3, 2, 7, 9] == [3, 2, 7, 9]
        if (finded_dna[i] == person[i+1]):
            find = True
        else:
            find = False
            # Force break and continue
            break

    # Check find boolean
    if find:
        print(person[0])
        exit()

# Check find boolean
if not find:
    print("No match")
