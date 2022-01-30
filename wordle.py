from functools import total_ordering
from random import choice

guesses_allowed = set()
possible_answers = []

with open("wordfiles/guesses_allowed.txt", "r") as f:
    for line in f:
        guesses_allowed.add(line.strip())

with open("wordfiles/possible_answers.txt", "r") as f:
    for line in f:
        possible_answers.append(line.strip())

answer = choice(possible_answers)

print("X means letter is not in the word")
print("^ means letter is in the word, but not in the right position")
print("= means letter is in the correct position")

# print(answer)

total_guesses = 0

guessed = False
while guessed == False:

    guess = input("What is your guess? ")
    while guess not in guesses_allowed:
        guess = input("That guess is not allowed. What is your guess?")

    total_guesses += 1

    print(guess)
    guessed = True
    for i, c in enumerate(guess):

        if answer[i] == c:
            print('=',end='')
        elif c not in answer:
            print('X',end='')
            guessed = False
        else:
            print('^',end='')
            guessed = False
    print()

print(f"It took you {total_guesses} total guesses.")
