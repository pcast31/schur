"""
This file contains all the tests used for functions in src/weak_schur.
Currently tests the fitness, verify_partition functions in specific,
"""

import timeit
import json
import cProfile
import matplotlib.pyplot as plt


from src.weak_schur import Partition, verify_partition, fitness

# importing a 6-color weakly-sum free partition
with open("data/partition6.json", "r", encoding="utf-8") as fp:
    partition6 = json.loads(fp.read())


def test_verify_partition(profile=False):
    """Calls verify_partition on partition6

    This is a test function that repeatedly verifies partition6
    i.e. if it is a weakly sum-free partition, and gets the results.

    Parameters
    ----------
    profile: bool
        Decides if the test should also output a profile of the function.

    Returns
    -------
    dict(num_iter, total_time)
        returns the time result(s) of `verify_partition`
    """

    # Verifying the run
    result = dict.fromkeys([10, 100, 500, 1000, 2500, 5000])
    for num_iter in result:
        result[num_iter] = timeit.timeit(
            lambda: verify_partition(partition6), number=num_iter
        )
        print(f"Partition for n={len(partition6)} ({num_iter}): {result[num_iter]}")

    # now plotting the time taken per iteration
    plt.subplot(1, 2, 1)
    plt.plot(result.keys(), list(result.values()))
    plt.grid()
    plt.title("Total time taken")

    plt.subplot(1, 2, 2)
    plt.plot(
        result.keys(),
        [result[num_iter] / num_iter for num_iter in result.items()]
    )
    plt.grid()
    plt.title("Time taken per iteration")

    plt.show()

    # profiling my verify_partition function
    if profile:
        cProfile.run("test_verify_partition()")

    return result


def test_verify_fitness():
    """This function tests both the verify and the fitness functions
    for our weakly sum-free partitions

    Fitness returns the number of pairs that violate the sum-free property
    of our potential partition, so a fitness of 0 => our partition is weakly
    sum-free.
    On the other hand, verify_partition simply checks if the argument is
    (or is not) weakly sum-free.
    """
    # The 1-partition, a trivial example.
    assert verify_partition(partition=[[1, 2]]) is True
    print(f"Fitness of the partition = {fitness([[1,2]])}")

    # This should fail ...
    assert verify_partition(partition=[[1, 2, 3, 5]]) is False
    assert fitness([[1,2,3,5]]) == 2
    print(f"Fitness of the partition = {fitness([[1,2,3,5]])}")

    # One possible 2-partition
    assert verify_partition(partition=[[1, 2], [3, 4]]) is True
    print(f"Fitness of the partition = {fitness([[1, 2], [3, 4]])}")

    # The largest possible 2-partition
    assert verify_partition(partition=[[1, 2, 4, 8], [3, 5, 6, 7]]) is True
    print(f"Fitness of the partition = { fitness([[1, 2, 4, 8], [3, 5, 6, 7]] )}")

    # Finally, we're checking a partition with 6 colors
    print(
        f"Verifying that partition_6 is a partition: {verify_partition(partition=partition6)}"
    )
    print(f"Fitness of the partition = {fitness(partition6)}")


def test_partition_class():
    """This function tests both the verify and the fitness functions
    for our weakly sum-free partitions

    Fitness returns the number of pairs that violate the sum-free property
    of our potential partition, so a fitness of 0 => our partition is weakly
    sum-free.
    On the other hand, verify_partition simply checks if the argument is
    (or is not) weakly sum-free.
    """
    # # The largest possible 2-partition
    my_partition = Partition([[1, 2, 4, 8], [3, 5, 6, 7]])

    # assert verify_partition(partition=my_partition) is True
    print(f"Fitness of the partition = { my_partition.score }")

    # adding an element to my_partition
    my_partition.single_add(elem=9, color=1)

    # Now, this should fail
    # assert verify_partition(partition=my_partition) is False
    print(f"Partition is now: {my_partition.partition}" )
    print(f"Fitness of the partition = { my_partition.score }; {fitness(my_partition.partition)}")
    assert fitness(my_partition.partition) == my_partition.score

if __name__ == "__main__":
    TEST_RESULT = test_verify_partition()
    test_verify_fitness()
    test_partition_class()
    with open("results/test_results.json", "w", encoding="utf-8") as fp:
        json.dump(TEST_RESULT, fp)
