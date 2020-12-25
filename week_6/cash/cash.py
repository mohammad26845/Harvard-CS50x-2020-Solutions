from cs50 import get_float

# Get total $
dollars = 0
while (dollars <= 0):
    dollars = get_float("Change owed: ")

# Round and transfer to cents (Dollars To Cents)
cents = round(dollars * 100, 0)
coins = 0

# Calculating the number of coins
coins += cents // 25
cents = cents % 25

coins += cents // 10
cents = cents % 10

coins += cents // 5
cents = cents % 5

coins += cents // 1
cents = cents % 1

# displays the total number of coins (float To Int)
print(int(coins))