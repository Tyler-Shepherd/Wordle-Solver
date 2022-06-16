from enum import Enum
import random

class Color(Enum):
    GRAY = 1
    YELLOW = 2
    GREEN = 3


def colorize(target, guess):
    colors = [Color.GRAY] * len(guess)

    for loc in range(len(target)):
        target_letter = target[loc]

        if guess[loc] == target_letter:
            colors[loc] = Color.GREEN
        elif target_letter in guess:
            guess_loc = next(
                (x for x in range(len(guess)) if guess[x] == target_letter and colors[x] == Color.GRAY), None)
            if guess_loc is not None:
                colors[guess_loc] = Color.YELLOW

    return colors



def is_possible(possible_word, colors, guess):
    # array that says when a letter in the possible word has been used to fulfill a color
    used = [False] * len(possible_word)

    for (pos, color) in enumerate(colors):
        guessed_letter = guess[pos]

        # all greens in same place
        if color == Color.GREEN:
            if possible_word[pos] != guessed_letter:
                return False
            used[pos] = True

    for (pos, color) in enumerate(colors):
        guessed_letter = guess[pos]
        if color == Color.YELLOW:
            # yellows not in the same place
            if possible_word[pos] == guessed_letter:
                return False

            # every yellow reused
            reused_yellow = next(
                (x for x in range(len(possible_word)) if possible_word[x] == guessed_letter and not used[x]), None)
            if reused_yellow is None:
                return False
            used[reused_yellow] = True

    for (pos, color) in enumerate(colors):
        guessed_letter = guess[pos]

        if color == Color.GRAY:
            # gray not in same spot
            if possible_word[pos] == guessed_letter:
                return False

            # no grays used anywhere
            used_gray = next(
                (x for x in range(len(possible_word)) if possible_word[x] == guessed_letter and not used[x]), None)
            if used_gray is not None:
                return False

        # test cases:
        # target is "lefty". first guess is "forte". says the 'e' is yellow
        # it should not try "lefte". even though there is an e in different place, the last e is in same

        # if you guess something with 2 'e's, and both are yellow
        # then every guess after has to have at least 2 'e's

        # if you guess 3 'e's and 2 are yellow
        # every guess after has to have exactly 2 'e's

        # target "cycle", guess "fiere". needs to do green first and not remove on first gray e

    return True

def all_green(colors):
    for i in colors:
        if i != Color.GREEN:
            return False

    return True


def map_input_to_colors(colors_input):
    return list(map(lambda x: Color(int(x)), colors_input))


def get_entropy(word, all_words):
    return random.random()


