import requests
from collections import defaultdict

server = "https://ctech-wordle-server.herokuapp.com/"
# server = "http://localhost:5000"


r = requests.post(server, json={
    'command': 'allwords'
})
# , Response: {r.json()}")
print(f"Status Code to get all words: {r.status_code}")

allwords = set(r.json()['answers'])

# r = requests.post(server, json={
#     'command': 'reload'
# })
# print(f"Status Code to reload: {r.status_code}, Response: {r.json()}")

r = requests.post(server, json={
    'command': 'newid',
    'nickname': 'jobartucz'
})
print(f"Status Code to get a new ID: {r.status_code}, Response: {r.json()}")
userid = r.json()['userid']


def solveword(wordid):

    global allwords
    global server
    global userid
    possible_answers = set(allwords)

    answer = [None, None, None, None, None]
    good_letters_no_pos = set()
    good_letters_wrong_pos = [set(), set(), set(), set(), set()]
    bad_letters = set()

    response = "0"
    while True:

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
            # print(f"The only answer left is {possible_answers}")
            guess = list(possible_answers)[0]
        else:
            guess = sorted(
                word_probs, key=word_probs.__getitem__, reverse=True)[0]

        r = requests.post(server, json={
            'command': 'guess',
            'userid': userid,
            'wordid': wordid,
            'guess': guess
        })

        if r.status_code != 200:
            return f"ERROR: {r.status_code}"
        elif 'ERROR' in r.json():
            print(f"Status Code: {r.status_code}, Response: {r.json()}")
            return 'ERROR'
        else:
            response = r.json()['result']

        if response == "11111":
            # print(f"FOUND: {guess}")
            return guess
        # else:
            # print(f"received: {response} for {guess}")

        for i, c in enumerate(response):
            if c == "1":
                answer[i] = guess[i]
                continue
            elif c == "2":
                good_letters_no_pos.add(guess[i])
                good_letters_wrong_pos[i].add(guess[i])
                continue
            else:
                bad_letters.add(guess[i])

    print(f"??? FOUND: {guess}")
    return guess


for i in range(10):
    r = requests.post(server, json={
        'command': 'newword',
        'userid': userid
    })

    if r.status_code != 200:
        print(f"* * * ERROR! Status Code: {r.status_code}")
        break
    elif 'ERROR' in r.json():
        print(f"Status Code: {r.status_code}, Response: {r.json()}")
        break
    else:
        wordid = r.json()['wordid']

    theanswer = solveword(wordid)
    # print(f"the answer for {wordid} is {theanswer}")

r = requests.post(server, json={
    'command': 'stats',
    'userid': userid
})
print(f"Status Code to get stats: {r.status_code}, Response: {r.json()}")
