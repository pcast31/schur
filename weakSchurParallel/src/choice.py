"""
This file implements all the choice functions I want to play with.
Each function has the signature: list[int] -> int i.e. it takes a
list of ints to choose from, and returns their chosen index, ideally
for a minimum index.
"""
import random


def min_random(array: list[int]) -> int:
    """Function randomly chooses and returns the index
    of one of the minimum solutions. Since this decides which
    color to add to, it helps create a partition with an
    even distribution of elements over each of its colors.

    Args:
        array (list[int]): The scores to choose from

    Returns:
        int: the randomly chosen index of the minimum element.
    """

    minimum = min(array)
    indices = [idx for idx, elem in enumerate(array) if elem == minimum]
    return random.choice(indices)
