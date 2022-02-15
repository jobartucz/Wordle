from concurrent.futures import process
from random import choice
from flask import Flask, request
from collections import defaultdict

guesses_allowed = set()
possible_answers = set()
with open("wordfiles/guesses_allowed.txt", "r") as f:
    for line in f:
        guesses_allowed.add(line.strip())

rehash = dict()
hashes = set()
with open("wordfiles/possible_answers.txt", "r") as f:
    for line in f:
        w = line.strip()
        possible_answers.add(w)
        rehash[hash(w)] = w
        hashes.add(hash(w))

# don't worry, the hashes are unique (phew)
# print(len(set(possible_answers)), len(set(rehash)))

guesses = dict()

users = set()
def process_guess(user, guess, key):
    return

with open("status.txt", "r") as f:
    for line in f:
        user, guess, key = line.split()
        process_guess(user, guess, key)


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    error = None
    cmd = request.args.get('cmd', '')
    print(cmd)
    user = request.args.get('user', '')
    print(user)

    if user == '':
        return "<p>user can not be empty</p>"
    else:
        print(f"User: {user}")

    if cmd == '':
        return "<p>cmd can not be empty</p>"
    else:
        print(f"Cmd: {cmd}")

    if cmd == 'new':

        if user not in users:
            new = choice(list(hashes))
            users.add(user)
            return "<p>" + str(new) + "</p>"
