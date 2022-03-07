""" weak_schur.py

This code is to compute the weak schur numbers,
with a view to parallelize it someday.
"""
import json
import numpy as np


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
            : int
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


def generate_partition(partition: list, num_colors: int, num_to_add: int) -> list:
    len_partition = len(partition)
    if num_colors < len_partition:
        # Don't need to do anything if we're looking
        # for a smaller partition than we have.
        return partition
    # Add space for new partitions
    for i in range(1, num_colors - len_partition + 1):
        partition[f"E{len_partition + i}"] = []

    print(partition)
    return partition


if __name__ == "__main__":
    with open("data/partition6.json", "r", encoding="utf-8") as fp:
        partition6 = json.loads(fp.read())
    print(f"Fitness of the partition = {fitness(partition6)}")
    generate_partition(partition6, 8)
