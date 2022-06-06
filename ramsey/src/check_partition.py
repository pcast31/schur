import itertools
import math
import sys

import tqdm


def math_comb(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def load_partition(filename):
    with open(filename) as file:
        lines = file.readlines()
    partition = []
    for line in lines:
        col = []
        for x in map(int, line.split()):
            col.append(x)
        if col:
            partition.append(col)
    return partition


def is_partition(partition, partition_size, n_colors):
    if len(partition) != n_colors:
        print(f"The partition uses {len(partition)} colors instead of {n_colors}.")
        return False
    partition = [set(color) for color in partition]
    numbers = set()
    for color in partition:
        numbers.update(color)
    if numbers != set(range(1, partition_size + 1)):
        missing = set(range(1, partition_size + 1)).difference(numbers)
        if missing:
            print(f"Numbers {sorted(missing)} are not in the partition.")
        else:
            supplement = numbers.difference(set(range(1, partition_size + 1)))
            print(f"The partition has size {partition_size} but contains numbers {sorted(supplement)}.")
        return False
    return True


def k_clique(subset, size, color):
    set_range = subset[-1] - subset[0] + 1
    table = bytearray([1] * set_range)
    for x in subset:
        if x >= set_range:
            break
        table[x] = 0
    for clique in tqdm.tqdm(itertools.combinations(subset, size - 1), total=math_comb(len(subset), size - 1)):
        try:
            for i, x in enumerate(clique, 1):
                for y in clique[i:]:
                    if table[y - x]:
                        raise StopIteration
            print(f"The partition induces a clique of size {size} in color {color}: {clique}.")
            return True
        except StopIteration:
            continue
    return False


def check_partition(partition, clique_sizes, partition_size):
    if not is_partition(partition, partition_size, len(clique_sizes)):
        return False
    for color, (subset, size) in enumerate(zip(partition, clique_sizes), 1):
        if k_clique(subset, size, color):
            return False
    print(f"The partition of [|1, {partition_size}|] into {len(clique_sizes)} subsets is valid.")
    return True


def main():
    filename = sys.argv[1]
    partition = load_partition(filename)
    try:
        filename = filename.split('/')[3]
    except IndexError:
        filename = filename.split('\\')[3]
    description = filename[2:-5]
    clique_sizes, partition_size = description.split(';')
    partition_size = int(partition_size)
    clique_sizes = list(map(int, clique_sizes.split(',')))
    check_partition(partition, clique_sizes, partition_size)


if __name__ == '__main__':
    main()
