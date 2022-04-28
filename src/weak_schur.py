""" weak_schur.py

This code is to compute the weak schur numbers,
with a view to parallelize it someday.
"""
import json
import bisect
from copy import deepcopy
import numpy as np
import choice
from utils import chunk


class Partition:
    """
    This class pairs each potential solution with
    its score, which can be updated automatically with
    each call to add_element.
    """

    def __init__(self, num_colors: int, partition: list[list[int]] = None) -> None:
        """Initialiser function for the Partition class.

        Args:
            num_colors (int): number of colors to create the partition for
            partition (list[list[int]]): the actual partition current instance will use
        """
        if partition:
            # If there's a given partition to copy,
            # Prefer to use this
            self.partition = deepcopy(partition)
            self.score = fitness(self.partition)
        elif num_colors > 0 and isinstance(num_colors, int):
            # But if num_colors is defined instead, use it
            # to define an empty partition of the right size.
            self.partition = [[] for _ in range(num_colors)]
            self.score = 0

    def count_difference(self, elem: int, color: int) -> int:
        """Function to count the number of pairs of the form
                a+ elem = b, where a,b in self.partition[color]

        Args:
            elem (int): the element that was just added
            color (int): the sub-set of the partition to which `elem` was added

        Returns:
            int: the number of pairs of the form a+elem=b
        """
        count = 0
        hash_list = dict.fromkeys(self.partition[color], 1)
        # now counting the pairs with a difference
        for num in self.partition[color]:
            if num == elem:
                continue
            if (num in hash_list) and ((num + elem) in hash_list):
                count = count + 1
        return count

    def count_sum(self, elem: int, color: int) -> int:
        """Function to count the number of pairs of the form
                a+b = elem, where a,b in self.partition[color]

        Args:
            elem (int): the element that was just added
            color (int): the sub-set of the partition to which `elem` was added

        Returns:
            int: the number of pairs of the form a+b=elem
        """
        count = 0
        hash_list = {}
        for idx in range(len(self.partition[color])):
            num = self.partition[color][idx]
            if (elem - num) in hash_list and (elem - num) != elem:
                count = count + 1
            else:
                hash_list[num] = idx
        return count

    def single_add(self, elem: int, color: int) -> bool:
        """Adds an element and automatically dynamically updates
        the fitness score of the partition.

        Args:
            elem (int): new number to add
            color (int): which partition to add it to

        Returns:
            bool: True if adding and updating score have
                  succeeded, False if we're adding to a
                  partition that doesn't exist.
        """
        # If the partition specified is outside the number
        # of partitions that we have, return False and
        # add nothing.
        if color > len(self.partition):
            print(f"Cannot add {elem} to subset {color}")
            return False

        # Otherwise, add it and update self._score
        # self.partition[color].append(elem)
        # Optimisation: sorted insert each time
        bisect.insort(self.partition[color], elem)

        # We only need to verify the pairs that are
        # created by the addition of `elem`. All prior
        # information has already been stored in
        # self._score.

        # First for pairs of the type a + elem = b \in partition_i
        # then for pairs of the type a + b = elem \in partition_i
        self.score += self.count_difference(elem=elem, color=color) + self.count_sum(
            elem=elem, color=color
        )

        return True

    def group_add(self, list_elem: list[int], color: int) -> bool:
        """Repeatedly calls self.single_add to add a list of elements
           to a single color in the partition. Inherits the failure
           conditions from single_add indirectly.

        Args:
            list_elem (list[int]): list of elements to add
            color (int): color to which the elements are to be added.

        Returns:
            bool: True if all elements were successfully added,
                  False if even one fails.
        """
        # Using this to check at each go.
        check_bit = True
        for elem in list_elem:
            # Capturing the success of the operation
            check_bit = self.single_add(elem, color=color)
            if not check_bit:
                # and terminating if not successful.
                return check_bit
        # Only make it here if all successful.
        return check_bit

    def spread_add(self, list_elem: list[int]) -> bool:
        """Adds an element to each color in the partition.
        Requires that the number of elements to add is equal to
        the number of colors.

        Args:
            list_elem (list[int]): _description_

        Returns:
            bool: _description_
        """
        # Break if the spread operation cannot be carried out.
        num_colors = len(self.partition)
        if num_colors != len(list_elem):
            print("NotEnoughColorsError: Spread_Add terminates.")
            return False

        # Using check_bit again
        check_bit = True

        # Adding one element to each color.
        for color in range(num_colors):
            check_bit = self.single_add(elem=list_elem[color], color=color)
            if not check_bit:
                # and terminating if not successful.
                return check_bit
        # Only make it here if all successful.
        return check_bit


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
        check_upper = np.triu(np.meshgrid(part, part), k=1).T.reshape(-1, 2)

        # Check if any of the sums are
        if np.any(np.isin(np.sum(check_upper, axis=1), part)):
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
    for subp in partition:
        if len(subp) < 3:
            continue  # No point in iterating, when no sum is possible

        # Get the unique pairs from which we form the sum
        check_upper = np.triu(np.meshgrid(subp, subp), k=1).T.reshape(-1, 2)

        # Check if any of the sums are
        fitness_sum = fitness_sum + np.sum(np.isin(np.sum(check_upper, axis=1), subp))
    return fitness_sum


def generate_partition(
    num_colors: int, max_num: int, fitness_choice=np.argmin
) -> tuple:
    """Greedy Function to generate weakly sum-free partitions
    of the first `max_num` numbers into `num_colors` colors

    The function does not guarantee a true partition, but it
    does guarantee to choose the one that minimises fitness.

    Parameters
    ----------
    num_colors : int
        the number of colors to partition our numbers into
    max_num    : int
        The maximum number of ints to add to the partition,
        starting from 1
    fitness_choice     : function
        The fitness_choice function to use when taking the best
        solution from each iteration. It must have the
        signature:
            fitness_choice: list(int) -> int
        If no option is specified, this defaults to
        `numpy.argmin`


    Returns
    -------
    best_solution, fitness_solutions[best_idx] : list
        the partition of `n` numbers into `num_colors` colors
        that minimizes the given fitness function, along with
        its associated fitness score.
    """
    num = 0
    best_solution = [[] for _ in range(num_colors)]
    solutions = [[] for _ in range(num_colors)]
    fitness_solutions = np.zeros(shape=(num_colors, 1), dtype=int)

    while num < max_num:
        # Add integers to partitions as long
        # as there are numbers to add.
        num = num + 1
        for idx in range(num_colors):
            # create the new candidate solution
            # for this iteration
            temp = deepcopy(best_solution)
            temp[idx].append(num)

            # add it to the list,
            # and evaluate its fitness
            solutions[idx] = temp
            fitness_solutions[idx] = fitness(temp)

        # Now, we choose the best one
        # from the iteration that just finished.
        best_idx = fitness_choice(fitness_solutions)
        best_solution = solutions[best_idx]

    print(f"Partition: {best_solution}")
    print(f"Fitness: {fitness_solutions[best_idx]}")
    return best_solution, fitness_solutions[best_idx]


def generate_partition_iterative(
    num_colors: int, max_num: int, fitness_choice=np.argmin
) -> Partition:
    """Greedy Function to generate weakly sum-free partitions
    of the first `max_num` numbers into `num_colors` colors

    The function does not guarantee a true partition, but it
    does guarantee to choose the one that minimises fitness.

    In addition, this uses the Partition class.

    Parameters
    ----------
    num_colors : int
        the number of colors to partition our numbers into
    max_num    : int
        The maximum number of ints to add to the partition,
        starting from 1
    fitness_choice     : function
        The fitness_choice function to use when taking the best
        solution from each iteration. It must have the
        signature:
            fitness_choice: list(int) -> int
        If no option is specified, this defaults to
        `numpy.argmin`


    Returns
    -------
    best_solution, fitness_solutions[best_idx] : list
        the partition of `n` numbers into `num_colors` colors
        that minimizes the given fitness function, along with
        its associated fitness score.
    """
    num = 0
    best_solution = Partition(partition=None, num_colors=num_colors)
    solutions = [Partition(num_colors=num_colors) for _ in range(num_colors)]
    fitness_solutions = np.zeros(shape=(num_colors, 1), dtype=int)

    while num < max_num:
        # Add integers to partitions as long
        # as there are numbers to add.
        num = num + 1
        for idx in range(num_colors):
            # create the new candidate solution
            # for this iteration, and add num to it.
            # single_add updates the score internally.
            temp = deepcopy(best_solution)
            temp.single_add(elem=num, color=idx)

            # add it to the list,
            solutions[idx] = temp
            fitness_solutions[idx] = temp.score

        # Now, we choose the best one
        # from the iteration that just finished.
        best_idx = fitness_choice(fitness_solutions)
        best_solution = solutions[best_idx]

    print(f"Partition: {best_solution.partition}")
    print(f"Fitness: {best_solution.score}")
    return best_solution

def generate_partition_multiproc(
    num_colors: int, max_num: int, fitness_choice=np.argmin
) -> Partition:
    """Parallelisable Function to generate weakly sum-free partitions
    of the first `max_num` numbers into `num_colors` colors

    The function does not guarantee a true partition, but it
    does guarantee to choose the one that minimises fitness.

    In addition, this uses the Partition class.

    This will split the numbers [1,...,max_num ] into chunks of 
    size `num_colors`. Then, it will try adding the rotations of
    each chunk, and hope to find a minima in these combinations.

    Parameters
    ----------
    num_colors : int
        the number of colors to partition our numbers into
    max_num    : int
        The maximum number of ints to add to the partition,
        starting from 1
    fitness_choice     : function
        The fitness_choice function to use when taking the best
        solution from each iteration. It must have the
        signature:
            fitness_choice: list(int) -> int
        If no option is specified, this defaults to
        `numpy.argmin`


    Returns
    -------
    best_solution, fitness_solutions[best_idx] : list
        the partition of `n` numbers into `num_colors` colors
        that minimizes the given fitness function, along with
        its associated fitness score.
    """
    best_solution = Partition(partition=None, num_colors=num_colors)
    solutions = [Partition(num_colors=num_colors) for _ in range(num_colors)]
    fitness_solutions = np.zeros(shape=(num_colors, 1), dtype=int)

    ### TODO
    # Here, we iterate by chunks of numbers: 
    for sub_chunk in chunk(range(1, max_num+1), num_colors):
        # For each iteration, we rotate the
        # sub_chunk, and get the one that 
        # gives the minimum fitness. 
        for idx in range(num_colors): 
            # As before, create a candidate 
            # solution but perform a spread_add 
            temp = deepcopy(best_solution)
            temp.spread_add(sub_chunk)

            # Get its information
            solutions[idx] = temp
            fitness_solutions[idx] = temp.score

            # Now, rotate the chunk to prepare 
            # for the next iteration 
            sub_chunk = sub_chunk[1:] + sub_chunk[:1]

        # Now, we choose again the best one
        # from the iteration that just finished.
        best_idx = fitness_choice(fitness_solutions)
        best_solution = solutions[best_idx]
    
    print(f"Partition: {best_solution.partition}")
    print(f"Fitness: {best_solution.score}")
    return best_solution

if __name__ == "__main__":
    # This is where we test-drive code that has already been verified.
    pass 
