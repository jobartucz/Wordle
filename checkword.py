# helper.py - helps you solve wordle problems
from collections import defaultdict

total_guesses = 1

answer = [None, None, None, None, None]
good_letters_no_pos = set()
good_letters_wrong_pos = [set(), set(), set(), set(), set()]
bad_letters = set()

guesses_allowed = set()
possible_answers = set()
with open("wordfiles/guesses_allowed.txt", "r") as f:
    for line in f:
        guesses_allowed.add(line.strip())

with open("wordfiles/possible_answers.txt", "r") as f:
    for line in f:
        possible_answers.add(line.strip())

# possible_answers = ['ample','apple','fffff','affle']

theword = ""
while theword not in possible_answers:
    theword = input("What is the word? ")
guess = "slate"


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
            if c in bad_letters:  # discard all possibilities with letters that aren't in the word
                new_possible_answers.discard(w)
                break
            # discard all possibilities without letters in the right places
            elif answer[i] and answer[i] != c:
                new_possible_answers.discard(w)
                break
            # alredy tried this letter in this position
            elif c in good_letters_wrong_pos[i]:
                new_possible_answers.discard(w)
                break

    # reset so we don't check already discarded ones
    possible_answers = set(new_possible_answers)
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
                # discard if the good letter is not in the missing spots
                new_possible_answers.discard(w)
                break

    # now we have the new list of possible words
    # reset so we don't check already discarded ones
    possible_answers = set(new_possible_answers)
    # print("Possibilities left: ")
    # for w in sorted(possible_answers):
    #     print(w,end=', ')
    # print()

    word_probs = dict()
    letter_counts = [defaultdict(int), defaultdict(
        int), defaultdict(int), defaultdict(int), defaultdict(int)]
    letter_sums = [0, 0, 0, 0, 0]
    letter_probs = [defaultdict(float), defaultdict(float), defaultdict(
        float), defaultdict(float), defaultdict(float)]

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
        return list(possible_answers)[0]

    return sorted(word_probs, key=word_probs.__getitem__, reverse=True)[0]


while guess != theword:

    print(guess)
    total_guesses += 1

    for i, c in enumerate(guess):

        if c == theword[i]:
            answer[i] = c
            continue
        elif c in theword:
            good_letters_no_pos.add(c)
            good_letters_wrong_pos[i].add(c)
            continue
        else:
            bad_letters.add(c)

    guess = recalc()

print(theword)
print(f"It took you {total_guesses} guesses")
