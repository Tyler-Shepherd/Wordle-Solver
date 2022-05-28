# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Ctrl+F8 to toggle the breakpoint.
import random
from enum import Enum


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


def get_words():
    file = open("./words.txt", 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    return lines

def all_green(colors):
    for i in colors:
        if i != Color.GREEN:
            return False

    return True


def print_colors(colors):
    to_print = ""
    for c in colors:
        if c == Color.GRAY:
            to_print += "GRAY "
        elif c == Color.YELLOW:
            to_print += "YELLOW "
        else:
            to_print += "GREEN "

    return to_print


def random_solve(target, words):
    num_iterations = 0

    while num_iterations < 100000:
        random_word = random.choice(words)
        colors = colorize(target, random_word)
        print(num_iterations, random_word, print_colors(colors))

        if all_green(colors):
            break

        num_iterations += 1

    return num_iterations


def is_possible(possible_word, colors, guess):
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


def random_hard_solve(target, words):
    num_iterations = 1
    guessable_words = set(words)

    while num_iterations < 1000:
        guess = random.choice(list(guessable_words))
        # if num_iterations == 1:
        #     guess = "hogen"
        # if num_iterations == 2:
        #     guess = "fiere"

        colors = colorize(target, guess)

        guessable_words.remove(guess)

        # go through guessable_words and remove all those that dont fit colors
        for possible_word in list(guessable_words):
            if not is_possible(possible_word, colors, guess):
                guessable_words.remove(possible_word)

        num_remaining = len(guessable_words)
        print(num_iterations, guess, print_colors(colors), num_remaining)
        if all_green(colors):
            break

        if num_remaining < 10:
            print(guessable_words)

        num_iterations += 1

    return num_iterations



def map_input_to_colors(colors_input):
    return list(map(lambda x: Color(int(x)), colors_input))


def solve_for_me(words):
    guessable_words = set(words)
    num_iterations = 1
    while num_iterations < 100:
        guess = random.choice(list(guessable_words))

        colors_input = input(str(num_iterations) + ". " + guess + ": ")
        colors = map_input_to_colors(colors_input)

        guessable_words.remove(guess)

        # go through guessable_words and remove all those that dont fit colors
        for possible_word in list(guessable_words):
            if not is_possible(possible_word, colors, guess):
                guessable_words.remove(possible_word)

        num_remaining = len(guessable_words)
        print(num_remaining)

        if num_remaining < 10:
            print(guessable_words)

        num_iterations += 1


def find_possible_words(words, colorsArr, guesses):
    guessable_words = set(words)
    for (index, colorsInput) in enumerate(colorsArr):
        colors = map_input_to_colors(colorsInput)
        guess = guesses[index]

        if guess in guessable_words:
            guessable_words.remove(guess)

        # go through guessable_words and remove all those that dont fit colors
        for possible_word in list(guessable_words):
            if not is_possible(possible_word, colors, guess):
                guessable_words.remove(possible_word)

    print(len(guessable_words))
    print(guessable_words)



if __name__ == '__main__':
    words = get_words()

    # all lower case for now
    target = "rebus"

    # iters = random_hard_solve(target, words)
    # print(target, iters)

    # solve_for_me(words)

    find_possible_words(words, [
        "13333"
    ], ["dingo"]
    )

    # print(is_possible("vulva", [Color.GRAY, Color.YELLOW, Color.GRAY, Color.GRAY, Color.GRAY], "bajra"))



