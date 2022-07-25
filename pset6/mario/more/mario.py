while True:
    try:
        height = int(input("Height: "))  # Ask user input
        if (0 < height < 9):  # Check user input validity
            break
    except ValueError:
        None
# output
for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i + "  " + "#" * i)