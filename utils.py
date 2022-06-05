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



# for fib we need to say:
# 1. it can't possibly be the color it says it is.
# 2. other spots have to consider that spot may be different color
    # so a gray s in non-fib spot doesn't mean theres no s anywhere. bc it could be yellow/green s in fib spot

def is_possible(possible_word, colors, guess, fib=None):
    # array that says when a letter in the possible word has been used to fulfill a color
    used = [False] * len(possible_word)
    used_fib = False

    for (pos, color) in enumerate(colors):
        guessed_letter = guess[pos]

        # all greens in same place
        if color == Color.GREEN:
            if pos == fib:
                if possible_word[pos] == guessed_letter:
                    return False
                continue

            if possible_word[pos] != guessed_letter:
                return False
            used[pos] = True

    for (pos, color) in enumerate(colors):
        if pos == fib:
            continue

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
            if pos == fib:
                used_fibbing_gray = next(
                    (x for x in range(len(possible_word)) if possible_word[x] == guessed_letter and not used[x]), None)
                if used_fibbing_gray is None:
                    # the letter that's fibbing as gray must be used somewhere
                    return False
                used[used_fibbing_gray] = True

                continue

            # gray not in same spot
            if possible_word[pos] == guessed_letter:
                return False

            # no grays used anywhere
            used_gray = next(
                (x for x in range(len(possible_word)) if possible_word[x] == guessed_letter and not used[x]), None)
            if used_gray is not None:
                if fib is not None and guess[fib] == guessed_letter and not used_fib:
                    # could be case that fibbing spot is non-gray for same letter, so there could be max 1 of the gray
                    used[used_gray] = True
                    used_fib = True
                else:
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
