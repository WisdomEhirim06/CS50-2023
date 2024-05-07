# TODO
from cs50 import get_float

def main():
    cents = get_cents()

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(cents)
    cents = cents - pennies * 1

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(coins)


#prompt user for cents
def get_cents():
    while True:
        try:
            cents = get_float("Change Owed: ")
            if cents > 0:
                return cents * 100
        except ValueError:
            print("Only numbers")

def calculate_quarters(cents):
    # Quarters keeps incrementing until it reaches 25
    quarters = 0
    while cents >= 25:
        quarters += 1
        cents = cents - 25
    return quarters

def calculate_dimes(cents):

    # Dimes is only 10, using a while loop
    dimes = 0
    while cents >= 10:
        dimes += 1
        cents = cents - 10
    return dimes


def calculate_nickels(cents):
    # We'll do the same for the rest
    # Nickels are 4 so
    nickels = 0
    while cents >= 5:
        nickels += 1
        cents = cents - 5
    return nickels


def calculate_pennies(cents):
    pennies = 0
    while cents >= 1:
        pennies += 1
        cents = cents - 1
    return pennies


main()