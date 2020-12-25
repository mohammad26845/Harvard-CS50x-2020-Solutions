# Readability

# get input about the text
s = input("Text: ")

# Vars
letters = 0
sentences = 0
words = 1
index = 0

# Counter
for i in range(len(s)):
    # Convert strings to ascii
    ascii_code = ord(s[i])

    if ((ascii_code >= 65 and ascii_code <= 90) or (ascii_code >= 97 and ascii_code <= 122)):
        letters += 1

    if ((ascii_code == 46) or (ascii_code == 33) or (ascii_code == 63)):
        sentences += 1

    if (ascii_code == 32):
        words += 1

# Calculating index of text
L = letters * 100 / words
S = sentences * 100 / words
index = round(0.0588 * L - 0.296 * S - 15.8)

# Finally outputs the results
if (index < 1):
    print("Before Grade 1")
elif (index > 16):
    print("Grade 16+")
else:
    print("Grade", index)