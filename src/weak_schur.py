""" weak_schur.py

This code is to compute the weak schur numbers,
with a view to parallelize it someday.
"""
import json
import numpy as np
from copy import deepcopy


def verify_partition(partition: list) -> bool:
    """This function verifies that a given partition of the first n numbers,
    forms a weakly sum-free partition.

    A weakly sum-free partition of the integers is a disjoint partition
    such that for every distinct a,b,c in each set, a+b = c is always false.

    Parameters
    ----------
    partition : np.array of np.array of ints
        This is a potential weakly sum-free partition of the first n integers.

    Returns
    -------
            : bool
            whether or not the given partition is a weakly sum-free partition
    """
    for part in partition:
        if len(part) < 3:
            continue  # No point in iterating, when no sum is possible

        # Get the unique pairs from which we form the sum
        check = np.triu(np.meshgrid(part, part), k=1).T.reshape(-1, 2)

        # Check if any of the sums are
        if np.any(np.isin(np.sum(check, axis=1), part)):
            return False
    return True


def fitness(partition: list) -> int:
    """This function returns the fitness of a given partition
    of the first n numbers, which should form a weakly sum-free partition.

    A weakly sum-free partition of the integers is a disjoint partition
    such that for every distinct a,b,c in each set, a+b = c is always false.

    Parameters
    ----------
    partition : np.array of np.array of ints
        This is a potential weakly sum-free partition of the first n integers.

    Returns
    -------
    fitness_num  : int
            The fitness score of the partition i.e. the number of pairs
            violating the sum-free property.
    """
    fitness_sum = 0
    for part in partition:
        if len(part) < 3:
            continue  # No point in iterating, when no sum is possible

        # Get the unique pairs from which we form the sum
        check = np.triu(np.meshgrid(part, part), k=1).T.reshape(-1, 2)

        # Check if any of the sums are
        fitness_sum = fitness_sum + np.any(np.isin(np.sum(check, axis=1), part))
    return fitness_sum


def generate_partition(num_colors: int, n: int, choice=np.argmin) -> tuple:
    """Function to generate a weakly sum-free partition
    of the first `n` numbers into `num_colors` colors

    The function does not guarantee a true partition, but it
    does guarantee to choose the one that minimises fitness.

    Parameters
    ----------
    num_colors : int
        the number of colors to partition our numbers into
    n : int
        The maximum number of ints to add to the partition,
        starting from 1
    choice: function
        The default choice function to use when taking
        the best solution from each iteration. It must have
        the signature:
            choice: list(int) -> int


    Returns
    -------
    (best_solution, fitness_score)
        the tuple of the best solution and the associated fitness.
    """
    num = 0
    best_solution = [[] for _ in range(num_colors)]
    solutions = [[] for _ in range(num_colors)]
    fitness_solutions = np.zeros(shape=(num_colors, 1), dtype=int)
    while num < n:
        # Add integers to partitions as long
        # as there are numbers to add.
        num = num + 1
        for idx in range(num_colors):
            # create the new candidate solution
            temp = deepcopy(best_solution)
            temp[idx].append(num)

            # add it to the list
            solutions[idx] = temp
            fitness_solutions[idx] = fitness(temp)

        # Now, we choose the best one
        best_solution = solutions[choice(fitness_solutions)]

    print(f"Partition: {best_solution}")
    print(f"Fitnesses: {fitness_solutions}")
    return best_solution


if __name__ == "__main__":
    with open("data/partition6.json", "r", encoding="utf-8") as fp:
        partition6 = json.loads(fp.read())
    print(f"Fitness of the partition = {fitness(partition6)}")
    result = generate_partition(num_colors=5, n=100)
    # print(f"Partition generated: {result}")
