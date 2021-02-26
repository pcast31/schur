import heapq
import os
import pickle
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


def load_partitions():
    _, _, groups = next(os.walk("./partitions/all_partitions/"))
    for group in tqdm.tqdm(groups):
        for partition in read_file(group):
            yield partition


def select_partitions(necessary_condition=None, fitness_function=None,
                      max_size=10_000):
    if necessary_condition is None:
        necessary_condition = lambda _: True
    if fitness_function is None:
        fitness_function = lambda _: 0
        stop_early = True
    else:
        stop_early = False

    heap = []
    counter = 0

    for partition in load_partitions():
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

    partition = [None] * len(heap)
    i = 1
    while heap:
        partitions[-i] = heapq.heappop(heap)
        i += 1
    return partitions
