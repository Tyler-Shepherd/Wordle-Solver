import random
from copy import copy

from utils import colorize, is_possible, Color, all_green, map_input_to_colors


class Fib:
    def __init__(self, position, offset):
        self.position = position
        self.offset = offset # offset is either 1 or 2 or None (for building tree and we dont know offset)

    def __repr__(self):
        stringRep = "Position: " + str(self.position)
        if self.offset:
            stringRep += "/ Offset: " + str(self.offset)
        return stringRep


def solve_fibble_base(words, colorize_fn, first_guess):
    num_iterations = 1
    lie_tree = [([], set(words))] # list of tuples (lie_positions, remaining_words)

    while num_iterations < 100:
        guessable_words = set()
        for (_, words) in lie_tree:
            guessable_words = guessable_words.union(words)

        if num_iterations == 1 and first_guess is not None:
            guess = first_guess
        else:
            guess = random.choice(list(guessable_words))

        colors = colorize_fn(guess, num_iterations)
        if colors is True:
            break

        new_lie_tree = []

        for guess_lie_pos in range(5):
            for (guess_fibs, guess_words) in lie_tree:
                new_words = copy(guess_words)
                new_fibs = copy(guess_fibs)

                if guess in new_words:
                    new_words.remove(guess)
                new_fibs.append(Fib(guess_lie_pos, None))

                for possible_word in list(new_words):
                    if not is_possible(possible_word, colors, guess, guess_lie_pos):
                        new_words.remove(possible_word)

                if len(new_words) > 0:
                    new_lie_tree.append((new_fibs, new_words))

        lie_tree = new_lie_tree

        for potential in lie_tree:
            if len(potential[1]) < 10:
                print(potential[0], potential[1])
            else:
                print(potential[0], len(potential[1]))

        num_iterations += 1


def solve_fibble_random(words, target, fibs):
    def colorize_fn(guess, num_iterations):
        print(num_iterations, guess)

        colors = colorize(target, guess)
        if all_green(colors):
            return True

        print("True colors:", colors)
        apply_lie(colors, fibs[num_iterations - 1])
        print("Fibbing colors:" ,colors, fibs[num_iterations - 1])
        return colors

    solve_fibble_base(words, colorize_fn, None)

def solve_for_me_fibble(words, first_guess):

    def colorize_fn(guess, num_iterations):
        colors_input = input(str(num_iterations) + ". " + guess + ": ")
        colors = map_input_to_colors(colors_input)
        return colors

    solve_fibble_base(words, colorize_fn, first_guess)


def apply_lie(colors, lie):
    curr_color = colors[lie.position]

    new_color_val = (curr_color.value - lie.offset) % 3
    if new_color_val == 0:
        new_color_val = 3

    colors[lie.position] = Color(new_color_val)
