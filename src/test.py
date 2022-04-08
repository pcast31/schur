"""
This file contains all the tests used for functions in src/weak_schur.
Currently tests the fitness, verify_partition functions in specific,
"""
import random
import timeit
import json
import cProfile
import matplotlib.pyplot as plt

from src.weak_schur import (
    Partition,
    verify_partition,
    fitness,
    generate_partition,
    generate_partition_iterative,
)

# random.seed(12345)

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
    plt.plot(result.keys(), [result[num_iter] / num_iter for num_iter in result])
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
    assert fitness([[1, 2, 3, 5]]) == 2
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


def test_verify_fitness_iterative():
    """This function tests the Partition class for our weakly
    sum-free partitions

    First, it checks the initialisation of each instance is correct.
    Then, it takes random number to add and asserts that each insert
    updates the score correctly, by measuring it against the
    naive fitness function's results.
    """

    list_test_partitions = [
        # partition  -- score
        [[1, 2]],  # 0
        [[1, 2, 3, 5]],  # 2
        [[1, 2], [3, 4]],  # 0
        [[1, 2, 4, 8], [3, 5, 6, 7]],  # 0
    ]
    list_test_scores = [0, 2, 0, 0, 0]
    # The 1-partition, a trivial example.
    for idx in range(len(list_test_partitions)):
        # checking initialisation
        part = Partition(list_test_partitions[idx])

        assert part.score == list_test_scores[idx]
        print("----------------------------------------")
        print(f"Partition to test: {part.partition}")
        print(f"Initial fitness of the partition = {part.score}")

        # now adding a number to check if it is correct.
        # First finding out where to add numbers from
        curr_max = 0
        for sub_l in part.partition:
            curr_max = max(curr_max, max(sub_l))

        colors = range(len(part.partition))
        test_numbers = list(range(curr_max + 1, curr_max + 10))
        random.shuffle(test_numbers)  # To change the order of addition

        for number in test_numbers:
            # add part to a random color
            part.single_add(elem=number, color=random.choice(colors))

            # and assert it's giving the right score
            print(f"Partition is: {part.partition}")
            print(f"Element added was :{number}")
            print(f"Current score is: {part.score}")
            print(f"Score supposed to be: {fitness(part.partition)}")
            assert part.score == fitness(part.partition)


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
    my_partition = Partition([[1, 2, 4, 8], [3, 5, 7, 9]])

    # assert verify_partition(partition=my_partition) is True
    print(f"Fitness of the partition = { my_partition.score }")

    # adding an element to my_partition
    my_partition.single_add(elem=6, color=1)

    # Now, this should fail
    # assert verify_partition(partition=my_partition) is False
    print(f"Partition is now: {my_partition.partition}")
    print(
        f"Fitness of the partition = { my_partition.score }; {fitness(my_partition.partition)}"
    )
    assert fitness(my_partition.partition) == my_partition.score


def test_compare_generate_partition():
    """This function tests the execution time of the naive and iterative-based algorithms.

    Returns:
        dict: Dictionary containing the naive and the iterative runtimes.
    """
    test_cases = [
        (max_num, num_color)
        for max_num in [200, 500, 1000]
        for num_color in [4, 5, 6]
    ]
    print(test_cases)
    iterative_results = []
    naive_results = []

    for test_case in test_cases:
        print(f'Test case: {test_case}')
        max_num, num_color = test_case
        
        # running naive ...
        t_naive_1 = timeit.default_timer()
        result_naive = generate_partition(num_colors=num_color, max_num=max_num)
        t_naive_2 = timeit.default_timer()
        print(f'Naive: {t_naive_2 - t_naive_1}')

        # and iterative ...
        t_iter_1 = timeit.default_timer()
        result_iterative = generate_partition_iterative(num_colors=num_color, max_num=max_num)
        t_iter_2 = timeit.default_timer()
        print(f'Iterative: {t_iter_2 - t_iter_1}')
        print('--------------------------------------------')

        # Assert we're doing things correctly.
        assert result_naive[1] == result_iterative.score
        
        # Storing the results ... 
        naive_results.append((test_case, t_naive_2 - t_naive_1))
        iterative_results.append((test_case, t_iter_2 - t_iter_1))

    # and plotting them for good measure
    _, ax = plt.subplots(1,1) 
    plt.plot([record[1] for record in naive_results], 'bo')
    plt.plot([record[1] for record in iterative_results], 'r*')
    plt.title('Comparision of Naive and Iterative algorithms')
    plt.legend(['Naive', 'Iterative'])
    ax.set_xticklabels([str(test_case) for test_case in [(0,0)]+test_cases], rotation = 45)
    plt.grid()
    plt.show()

    # Now writing it to a file for later use 
    with open("results/test_compare_generate_partition.txt", "a") as fd:
        fd.write("Naive:\n")
        fd.write(json.dumps(naive_results))
        fd.write('\n')
        fd.write("Iterative:\n")
        fd.write(json.dumps(iterative_results))
        fd.write("\n-----------------------------------------------\n")

    return {"Naive": naive_results, "Iterative": iterative_results}


if __name__ == "__main__":
    TEST_RESULT = test_verify_partition()
    test_verify_fitness()
    test_partition_class()
    with open("results/test_results.json", "w", encoding="utf-8") as fp:
        json.dump(TEST_RESULT, fp)
