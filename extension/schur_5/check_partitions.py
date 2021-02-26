from load_partitions import load_partitions


def is_partition(partition):
    occurences = [1] + [0] * 160
    for subset in partition:
        for num in subset:
            occurences[num] += 1
    return all(map(lambda n_occu: n_occu == 1, occurences))


def is_sum_free(subset):
    list_subset = sorted(subset)
    set_subset = set(subset)
    maxi = list_subset[-1]
    for i, num in enumerate(list_subset):
        if 2 * num > maxi:
            break
        for j in range(i, len(list_subset)):
            add = num + list_subset[j]
            if add > maxi:
                break
            if add in set_subset:
                return False
    return True


def is_sum_free_partition(partition):
    return is_partition(partition) and all(map(is_sum_free, partition))


def main():
    c = 0
    for partition in load_partitions():
        minis = list(map(min, partition))
        assert minis == sorted(minis)
        assert is_sum_free_partition(partition)
    print(c, "partitions")


if __name__ == '__main__':
    main()
