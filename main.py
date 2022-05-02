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
            guess_loc = next((x for x in range(len(guess)) if guess[x] == target_letter and colors[x] == Color.GRAY), None)
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


def random_hard_solve(target, words):
    num_iterations = 0
    guessable_words = set(words)
    known_greens = set()
    known_yellows = set()
    known_grays = set()

    while num_iterations < 1000:
        guess = random.choice(list(guessable_words))
        colors = colorize(target, guess)
        print(num_iterations, guess, print_colors(colors))

        if all_green(colors):
            break

        guessable_words.remove(guess)

        for c, color in enumerate(colors):
            guessed_letter = guess[c]
            if color == Color.GREEN:
                known_greens.add((c, guessed_letter))
            elif color == Color.YELLOW:
                known_yellows.add((c, guessed_letter))
            else:
                known_grays.add(guessed_letter)

        for possible_word in list(guessable_words):
            should_remove = False

            # all greens in same place
            for (pos, letter) in known_greens:
                if possible_word[pos] != letter:
                    should_remove = True

            # all yellow letters in different places
            for (pos, letter) in known_yellows:
                yellow_letter_pos = possible_word.find(letter)
                if yellow_letter_pos == -1 or yellow_letter_pos == pos:
                    should_remove = True

                # this doesnt work for repeated letters
                # for example: target is "lefty". first guess is "forte". says the 'e' is yellow
                # it should not try "lefte". even though there is an e in different place, the last e is in same

                # other issue: if you guess something with 2 'e's, and both are yellow
                # then every guess after has to have at least 2 'e's

                # or if you guess 3 'e's and 2 are yellow
                # every guess after has to have exactly 2 'e's

                # so we cant keep a big set on per-letter basis. has to be per-guess with context of rest of guess


            # no gray letters

            if should_remove:
                guessable_words.remove(possible_word)

        num_iterations += 1

    return num_iterations




if __name__ == '__main__':
    words = get_words()

    # all lower case for now
    target = "lefty"

    iters = random_hard_solve(target, words)

    print(target, iters)

