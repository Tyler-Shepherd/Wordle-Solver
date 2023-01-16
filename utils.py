from enum import Enum
import math
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


def is_good_coloring(colors, guess):
    for (pos, color) in enumerate(colors):
        if color == Color.YELLOW:
            letter = guess[pos]

            # there cant be any grays of the same letter before a yellow
            for (i, x) in enumerate(guess):
                if x == letter and colors[i] == Color.GRAY and i < pos:
                    return False

    # this does not cover all cases, there are other bad possible colorings
    # like for example [Yellow, Green] is not possible since theres nowhere for the Yellow letter to go
    # but is_possible will cover those cases, since there wont be any words that match that pattern
    # whereas there are words that could match [Gray, Gray, Yellow] when guessing "baa" (the way is_possible is written), like "abb"

    return True


def all_green(colors):
    for i in colors:
        if i != Color.GREEN:
            return False

    return True


def map_input_to_colors(colors_input):
    return list(map(lambda x: Color(int(x)), colors_input))


all_colors = None
def all_color_arrangements():
    global all_colors

    if all_colors is not None:
        return all_colors

    def color_recur(so_far):
        if len(so_far) == 5:
            return [so_far]

        with_gray = so_far.copy()
        with_gray.append(Color.GRAY)
        with_yellow = so_far.copy()
        with_yellow.append(Color.YELLOW)
        with_green = so_far.copy()
        with_green.append(Color.GREEN)

        recurred_colors = color_recur(with_gray)
        recurred_colors.extend(color_recur(with_yellow))
        recurred_colors.extend(color_recur(with_green))
        return recurred_colors

    all_colors = color_recur([])
    return all_colors



def get_entropy(word, remaining_words):
    color_arrangements = all_color_arrangements()

    entropy = 0
    for colors in color_arrangements:
        if not is_good_coloring(colors, word):
            continue

        possible_words = list(filter(lambda w: is_possible(w, colors, word), remaining_words))
        p = len(possible_words) / len(remaining_words)

        if len(possible_words) == 0:
            continue

        value = p * -math.log2(p)

        entropy += value

    return entropy


