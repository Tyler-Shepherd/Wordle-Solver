import math
import random
from copy import copy

from utils import colorize, is_possible, Color, all_green, map_input_to_colors, all_color_arrangements, is_good_coloring


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
        print(len(guessable_words))

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

                colors_lie_1 = copy(colors)
                apply_lie(colors_lie_1, Fib(guess_lie_pos, 1))
                colors_lie_2 = copy(colors)
                apply_lie(colors_lie_2, Fib(guess_lie_pos, 2))

                for possible_word in list(new_words):
                    # check if possible if the lying color is either of the other two colors
                    is_possible_1 = is_possible(possible_word, colors_lie_1, guess)
                    is_possible_2 = is_possible(possible_word, colors_lie_2, guess)

                    if not is_possible_1 and not is_possible_2:
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


def get_entropy_fibble(word, remaining_words):
    color_arrangements = all_color_arrangements()
    color_arrangements_with_fibs = []

    for ar in color_arrangements:
        for i in range(5):
            color_arrangements_with_fibs.append((ar, Fib(i,1)))
            color_arrangements_with_fibs.append((ar, Fib(i,2)))

    entropy = 0
    for (colors, fib) in color_arrangements_with_fibs:
        # idk what to do with this
        # if not is_good_coloring(colors, word):
        #     continue

        copy_colors = copy(colors)
        apply_lie(copy_colors, fib)
        possible_words = list(filter(lambda w: is_possible(w, copy_colors, word), remaining_words))
        p = len(possible_words) / len(remaining_words)

        if len(possible_words) == 0:
            continue

        value = p * -math.log2(p)

        entropy += value

    return entropy