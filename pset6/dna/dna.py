from sys import argv
import csv
import re

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

with open(argv[1]) as csvfile:  # read the sequences from the DNA database
    reader = csv.reader(csvfile)

    for i, row in enumerate(reader):
        if i == 0:

            with open(argv[2], "r") as file:  # read the dna sequence from the file

                # compute longest run of STR which repeats in sequence
                strings = next(file)
                most_STR = []

                for i in range(1, len(row)):      # Loop through sequence to find STR

                    sequence = row[i]
                    adjust = (match[0] for match in re.finditer(fr"(?:{sequence})+", strings))

                    try:
                        STR = int(len(max(adjust, key=len)) / len(sequence))
                        most_STR.append(STR)

                    except ValueError:
                        most_STR.append(0)
        else:
            list_STR = list(map(int, row[1:]))

            if list_STR == most_STR:
                print(row[0])
                break
    else:
        print("No match")