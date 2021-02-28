import heapq
import os
import pickle
import random
import tqdm


def from_int(int_repr):
    partition = [[] for _ in range(5)]
    for n in range(1, 161):
        int_repr //= 5
        i = int_repr % 5
        partition[i].append(n)
    return partition


def read_file(filename):
    if isinstance(filename, int):
        filename = "{:05d}".format(filename)

    with open("./partitions/all_partitions/" + filename, 'rb') as file:
        partitions = pickle.load(file)
    return map(from_int, partitions)


def load_partitions(n_groups=None, take_first=True):
    _, _, groups = next(os.walk("./partitions/all_partitions/"))

    if not take_first:
        random.shuffle(groups)
    if n_groups is None:
        n_groups = len(groups)
    if isinstance(n_groups, float):
        n_groups = round(n_groups * len(groups))
    groups = groups[:n_groups]

    for group in tqdm.tqdm(groups):
        for partition in read_file(group):
            yield partition


def select_partitions(necessary_condition=None, fitness_function=None,
                      max_size=None, n_groups=None, take_first=True):
    if necessary_condition is None:
        necessary_condition = lambda _: True
    if fitness_function is None:
        fitness_function = lambda _: 0
        stop_early = True
    else:
        stop_early = False
    if max_size is None:
        max_size = 3_000_000_000

    heap = []
    counter = 0

    for partition in load_partitions(n_groups, take_first):
        if not necessary_condition(partition):
            continue

        counter += 1
        fitness = fitness_function(partition)
        item = (fitness, counter, partition)

        if len(heap) < max_size:
            heapq.heappush(heap, item)
        else:
            if stop_early:
                break
            heapq.heappushpop(heap, item)

    partitions = [None] * len(heap)
    i = 1
    while heap:
        partitions[-i] = heapq.heappop(heap)[-1]
        i += 1
    return partitions
