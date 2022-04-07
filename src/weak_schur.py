""" weak_schur.py

This code is to compute the weak schur numbers,
with a view to parallelize it someday.
"""
import json
from copy import deepcopy
import bisect 
import numpy as np
from pyparsing import col


class Partition:
    """
    This class pairs each potential solution with
    its score, which can be updated automatically with
    each call to add_element.
    """
    def __init__(self, partition = [[1,2], [3]] ) -> None:
        self.partition = deepcopy(partition)
        self.score = fitness(self.partition)

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
        hashList = dict.fromkeys(self.partition[color], 1)
        # now counting the pairs with a difference   
        for num in self.partition[color]: 
            if num == elem: 
                continue
            if (num in hashList) and \
                ((num + elem) in hashList):
                count  = count + 1
        return count

    def count_sum (self, elem: int, color: int) -> int: 
        """Function to count the number of pairs of the form
                a+b = elem, where a,b in self.partition[color]

        Args:
            elem (int): the element that was just added
            color (int): the sub-set of the partition to which `elem` was added

        Returns:
            int: the number of pairs of the form a+b=elem
        """
        count = 0
        hashList = {}
        for idx in range(len(self.partition[color])): 
            num = self.partition[color][idx]
            if (elem - num) in hashList \
                and (elem - num) != elem: 
                count = count + 1
            else:
                hashList[num] = idx 
        return count 
        # then for pairs of the type a + b = elem \in partition_i
        # which can be resolved as elem - b = a \in partition_i 
        # check_upper = np.unique([elem - x for x in self.partition[color]])
        # print(f"Upper:{check_upper}")
        # return np.sum(np.isin(check_upper, self.partition[color])) // 2

    def single_add(self, elem : int, color : int) -> bool:
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
        bisect.insort(self.partition[color], elem); 

        # We only need to verify the pairs that are
        # created by the addition of `elem`. All prior
        # information has already been stored in
        # self._score.

        # First for pairs of the type a + elem = b \in partition_i
        # then for pairs of the type a + b = elem \in partition_i
        # Note: We need to count each such pair only once! 
        #       So we use the or to do that job.  
        self.score += \
                self.count_difference(elem=elem, color=color) + \
                self.count_sum(elem=elem, color=color)

        return True


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

def fitness_iterative (part: Partition, elem: int, color: int) -> int: 
    if color > len(part.partition):
        print(f"Cannot add {elem} to subset {color}")
        return False

    # Otherwise, add it and update self._score
    # self._partition[color].append(elem)
    # Optimisation: sorted insert each time
    bisect.insort(part.partition[color], elem); 

    # We only need to verify the pairs that are
    # created by the addition of `elem`. All prior
    # information has already been stored in
    # self._score.

    # First for pairs of the type a + elem = b \in partition_i
    # then for pairs of the type a + b = elem \in partition_i
    # Note: We need to count each such pair only once! 
    #       So we use the or to do that job.  
    # required = {}
    # count = 0
    # for idx in range(len(part.partition[color])): 
    #     check_num = elem - part.partition[color][idx]
    #     if (abs(check_num) in required):# and elem != abs(check_num): 
    #         count = count + 1
    #     else :
    #         required[part.partition[color][idx]] = idx
    # part.score += count
    count = 0
    part.partition[color].sort()
    hashList = dict.fromkeys(part.partition[color], 1)
    for num in part.partition[color]: 
        # to count the differences ...
        if (num != elem) and ((num + elem) in hashList):
            count  += 1
    part.score += count 
    
    return part.score

def generate_partition(num_colors: int, max_num: int, choice=np.argmin) -> tuple:
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
    choice     : function
        The choice function to use when taking the best
        solution from each iteration. It must have the
        signature:
            choice: list(int) -> int
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
        best_idx = choice(fitness_solutions)
        best_solution = solutions[best_idx]

    print(f"Partition: {best_solution}")
    print(f"Fitness: {fitness_solutions[best_idx]}")
    return best_solution, fitness_solutions[best_idx]


if __name__ == "__main__":

    # Loading the 6-color partition, and testing it.
    with open("data/partition6.json", "r", encoding="utf-8") as fp:
        partition6 = json.loads(fp.read())
    print(f"Fitness of the 6-color partition = {fitness(partition6)}")

    # Now test-driving the generate_partition function using
    # user inputs.
    num_elems, num_color = [
        int(x) for x in input("Enter max. numbers and number of colors: ").split()
    ]
    result = generate_partition(num_colors=num_color, max_num=num_elems)
