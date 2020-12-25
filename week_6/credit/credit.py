# Statics
AE1 = "34"
AE2 = "37"
MC1 = "51"
MC2 = "52"
MC3 = "53"
MC4 = "54"
MC5 = "55"
Visa = "4"

# Vars
sum1 = 0
sum2 = 0
temp_int = 0

# get input from the user
card_num = input("Number: ")

# Calculating len of input
card_len = len(card_num)
brand = "INVALID"

# Compare first 2 digits to the brands
if (card_len == 13):
    if (card_num[:1] == Visa):
        brand = "VISA"

elif (card_len == 15):
    if (card_num[:2] == AE1 or card_num[:2] == AE2):
        brand = "AMEX"

elif (card_len == 16):
    if (card_num[:2] == MC1 or card_num[:2] == MC2 or card_num[:2] == MC3 or card_num[:2] == MC4 or card_num[:2] == MC5):
        brand = "MASTERCARD"
    elif (card_num[:1] == Visa):
        brand = "VISA"

else:
    print("INVALID")
    # End the program
    exit()


# Change string to int
card_num = int(card_num)

# Checksum input
while(card_num > 0):

    # Remove last digit and add to sum1
    sum1 += card_num % 10
    card_num = card_num // 10

    # Remove second last digit
    temp_int = (card_num % 10)*2
    card_num = card_num // 10

    # If the number is greater than 10 (sum of the first digit and the second digit)
    # For example 12 ==> 1+2 , 3 ==> 3+0
    sum2 += (temp_int % 10)+(temp_int // 10)

# if it validates the Algorithm prints result
if ((sum1 + sum2) % 10 == 0):
    print(brand)

else:
    print("INVALID")