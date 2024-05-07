# TODO

# prints a descending # block
def main():
    height = get_height()
    for i in range(height):
        # decrements space value
        for j in range(height-i-1):
            print(" ", end="")
        # increments hash
        for k in range(i+1):
            print("#", end="")

        print()

# prompts from height continuously till condition is met


def get_height():
    while True:
        try:
            height = int(input("Height: "))
            # height must be postive and less than 8
            if height > 0 and height <= 8:
                return height
        except ValueError:
            print("Not an integer")


main()