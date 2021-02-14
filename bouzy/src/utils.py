"""
Useful functions that do not belong to any other module.
"""


def is_partition(partition):
    """
    Checks whether partition is indeed a partition of [|1, N|]. N is defined as
    the greatest integer of the elements of partition.

    Parameter
    ---------
    partition : iterable of iterable of int

    Returns
    -------
    bool

    """
    max_n = max(max(subset, default=0) for subset in partition)
    occurences = [1] + [0] * max_n
    for subset in partition:
        for num in subset:
            occurences[num] += 1
    return all(map(lambda n_occu: n_occu == 1, occurences))


def is_weakly_sum_free(subset):
    """
    Checks whether subset is weakly sum free, that is for every a and b in
    subset, a + b does not belong to subset.

    Parameter
    ---------
    subset : iterable of int

    Returns
    -------
    bool

    """
    if not subset:
        return True
    list_subset = sorted(subset)
    set_subset = set(subset)
    maxi = list_subset[-1]
    for i, num in enumerate(list_subset):
        if 2 * num > maxi:
            break
        for j in range(i + 1, len(list_subset)):
            add = num + list_subset[j]
            if add > maxi:
                break
            if add in set_subset:
                return False
    return True


def is_weakly_sum_free_partition(partition):
    """
    Checks whether partition is indeed a partition (see is_partition) and
    whether each of its subsets is is weakly sum free (see is_weakly_sum_free).

    Parameter
    ---------
    partition : iterable of iterable of int

    Returns
    -------
    bool

    """
    return is_partition(partition) and all(map(is_weakly_sum_free, partition))
