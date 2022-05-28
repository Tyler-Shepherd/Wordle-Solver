import random

from utils import colorize, is_possible, Color


class Fib:
    def __init__(self, position, offset):
        self.position = position
        self.offset = offset # offset is either 1 or 2

    def __str__(self):
        return "Position: " + str(self.position) + "/ Offset: " + str(self.offset)


def solve_fibble_random(words, target, fibs):
    target = "blank"
    guess = "brank"
    colors = colorize(target, guess)

    apply_lie(colors, fibs[0])

    return


    num_iterations = 1
    lie_tree = [([], set(words))] # list of tuples (lie_positions, remaining_words)
    # lie_tree = [([], set(["a", "b"])), ([], set(["a", "c", "d"])), ([], set(["a", "e"]))]

    while num_iterations < 10:
        guessable_words = set()
        for (_, words) in lie_tree:
            guessable_words = guessable_words.union(words)
        guess = random.choice(list(guessable_words))

        print(guess)

        colors = colorize(target, guess)

        for (_, words) in lie_tree:
            words.remove(guess)
            for possible_word in list(words):
                if not is_possible(possible_word, colors, guess):
                    words.remove(possible_word)

        num_iterations += 1

def apply_lie(colors, lie):
    curr_color = colors[lie.position]

    print(colors)
    print(lie)
    new_color_val = (curr_color.value - lie.offset) % 3
    if new_color_val == 0:
        new_color_val = 3

    colors[lie.position] = Color(new_color_val)

    print(colors)

