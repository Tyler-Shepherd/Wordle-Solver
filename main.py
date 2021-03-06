# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Ctrl+F8 to toggle the breakpoint.
import random

from fibble import solve_fibble_random, Fib, solve_for_me_fibble
from utils import Color, colorize, is_possible, all_green, map_input_to_colors, get_entropy


def get_words():
    file = open("./words.txt", 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    return lines




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


def hard_solve_base(words, colorize_fn, choose_guess_fn):
    num_iterations = 1
    guessable_words = set(words)

    while num_iterations < 1000:
        guess = choose_guess_fn(guessable_words)
        colors = colorize_fn(guess, num_iterations)

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


def random_hard_solve(target, words):
    def colorize_fn(guess, num_iterations):
        return colorize(target, guess)

    def choose_guess_fn(guessable_words):
        return random.choice(list(guessable_words))

    return hard_solve_base(words, colorize_fn, choose_guess_fn)


def info_theory_solve(target, words):
    def colorize_fn(guess, num_iterations):
        return colorize(target, guess)

    def choose_guess_fn(guessable_words):
        entropies = []

        count = 0
        for word in guessable_words:
            entropy = get_entropy(word, guessable_words)
            entropies.append((word, entropy))
            count += 1

            print(count, word, entropy)

        entropies.sort(reverse=True, key=lambda x: x[1])

        for i in range(min(len(entropies), 5)):
            print("\t", entropies[i])

        return entropies[0][0]

    return hard_solve_base(words, colorize_fn, choose_guess_fn)




def solve_for_me_random(words):
    def colorize_fn(guess, num_iterations):
        colors_input = input(str(num_iterations) + ". " + guess + ": ")
        return map_input_to_colors(colors_input)

    def choose_guess_fn(guessable_words):
        return random.choice(list(guessable_words))

    return hard_solve_base(words, colorize_fn, choose_guess_fn)


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
    target = "primo"

    iters = info_theory_solve(target, words)
    print(target, iters)

    # solve_for_me_random(words)

    # find_possible_words(words, [
    #     "12112", "11311"
    # ], ["color", "blind"]
    # )

    # print(is_possible("palsy", [Color.GRAY, Color.GRAY, Color.YELLOW, Color.YELLOW, Color.GRAY], "trass"))
    # print(is_possible("palsy", [Color.GRAY, Color.GRAY, Color.YELLOW, Color.GREEN, Color.GRAY], "trass"))

    # solve_fibble_random(words, "exist", [Fib(2,1), Fib(3,1), Fib(1,1), Fib(2,1), Fib(0,1), Fib(1,2), Fib(3,1), Fib(2,2), Fib(1,1)])

    # solve_for_me_fibble(words, "folly")