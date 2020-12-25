# Mario LESS
# You can also use the following functions.
# from cs50 import get_int
# height = get_int("Height:\n")

# The first definition of height
height = 0

# Check input
while True:
    height = input("Height:\n")
    # Check digit input
    if height.isdigit():
        # Convert STR to INT
        height = int(height)

        if height > 0 and height <= 8:

            # prints a pyramid of hashes
            for i in range(1, height + 1):
                print(" " * (height - i), end="")
                print("#" * (i))
            break