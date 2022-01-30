# helper.py - helps you solve wordle problems
from collections import defaultdict

guesses_allowed = set()
possible_answers = set()
total_guesses = 1

answer = [None,None,None,None,None]
good_letters_no_pos = set()
good_letters_wrong_pos = [set(),set(),set(),set(),set()]
bad_letters = set()

with open("wordfiles/guesses_allowed.txt", "r") as f:
    for line in f:
        guesses_allowed.add(line.strip())

with open("wordfiles/possible_answers.txt", "r") as f:
    for line in f:
        possible_answers.add(line.strip())

# possible_answers = ['ample','apple','fffff','affle']

def recalc():

    global possible_answers, guesses_allowed, answer, bad_letters, good_letters_no_pos

    if None not in answer:
        print(f"The answer is {''.join(answer)}")
        return True

    for c in answer:
        good_letters_no_pos.discard(c)

    new_possible_answers = set(possible_answers)
    for w in possible_answers:

        for i, c in enumerate(w):
            if c in bad_letters: # discard all possibilities with letters that aren't in the word
                new_possible_answers.discard(w)
                break
            elif answer[i] and answer[i] != c: # discard all possibilities without letters in the right places
                new_possible_answers.discard(w)
                break
            elif c in good_letters_wrong_pos[i]: # alredy tried this letter in this position
                new_possible_answers.discard(w)
                break


    possible_answers = set(new_possible_answers) # reset so we don't check already discarded ones
    for w in possible_answers:
        # this is not perfect yet, could do more with positioning
        for l in good_letters_no_pos:

            # look for the letter in the empty spaces
            found = False 
            for i, c in enumerate(w):
                if answer[i]:
                    continue
                if c == l:
                    found = True
                    break

            if found == False:
                new_possible_answers.discard(w) # discard if the good letter is not in the missing spots
                break

    # now we have the new list of possible words
    possible_answers = set(new_possible_answers) # reset so we don't check already discarded ones
    # print("Possibilities left: ")
    # for w in sorted(possible_answers):
    #     print(w,end=', ')
    # print()

    word_probs = dict()
    letter_counts = [defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)]
    letter_sums = [0,0,0,0,0]
    letter_probs = [defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float)]

    for w in possible_answers:
        for i, c in enumerate(w):
            letter_sums[i] += 1
            letter_counts[i][c] += 1

    for i in range(5):

        # if we already have the answer, it's 100%
        if answer[i]:
            letter_probs[i][answer[i]] = 1
            continue

        # otherwise, calculate the probability
        for c in letter_counts[i].keys():
            if letter_probs[i][c] != 1:
                letter_probs[i][c] = letter_counts[i][c] / letter_sums[i]

    for w in possible_answers:
        prob = 0
        for i, c in enumerate(w):
            prob += letter_probs[i][c]
        word_probs[w] = prob

    if len(possible_answers) == 1:
        print ("The answer is " + list(possible_answers)[0])
        return True

    i = 0
    for w in sorted(word_probs, key=word_probs.__getitem__, reverse=True):
        i += 1
        if i == 10:
            break
        print(f"{w}: {int(word_probs[w]*100/5)}%")

    return False

while True:
    if recalc() == True:
        print(f"It took you {total_guesses} total guesses.")
        break

    guess = input("What is your guess? ")
    while guess not in guesses_allowed:
        print("*** That is not in the list of allowed guesses. ***")
        guess = input("What is your guess? ")

    total_guesses += 1

    for i, c in enumerate(guess):
        print(f"Type 1 if it was the correct letter in correct position, 2 if it was a correct letter in the wrong position, or 3 if the letter is not in the word")
        ans = input(f"'{c}' at position {i+1} [1/2/3]: ")
        if ans == '1':
            answer[i] = c
            continue
        elif ans == '2':
            good_letters_no_pos.add(c)
            good_letters_wrong_pos[i].add(c)
            continue
        else:
            bad_letters.add(c)
