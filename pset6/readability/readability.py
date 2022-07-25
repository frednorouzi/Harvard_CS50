import re
import string

txt = input("Text: ")  # asking user input

num_l = len(re.findall('[a-zA-Z]', txt))  # Count number of letters
num_w = len(txt.split())  # Count number of words
num_s = len(re.findall(r'[.!?]+', txt))  # Count number of sentences

L = (num_l * 100.0) / num_w
S = (num_s * 100.0) / num_w

grade = round(0.0588 * L - 0.296 * S - 15.8)

# output
if grade < 1:
    print("Before Grade 1")
elif grade > 15:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
