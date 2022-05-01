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

    while num_iterations < 1000:
        guess = random.choice(list(guessable_words))
        colors = colorize(target, guess)
        print(num_iterations, guess, print_colors(colors))

        if all_green(colors):
            break

        guessable_words.remove(guess)

        for word in list(guessable_words):
            should_remove = False
            for c, color in enumerate(colors):
                # all greens in same place
                if color == Color.GREEN:
                    if word[c] != guess[c]:
                        should_remove = True
                        break

                # all yellow letters in different places

                # no gray letters


                # except this also needs to consider all previous guesses

            if should_remove:
                guessable_words.remove(word)

        num_iterations += 1

    return num_iterations




if __name__ == '__main__':
    words = get_words()

    # all lower case for now
    target = "lefty"

    iters = random_hard_solve(target, words)

    print(target, iters)

