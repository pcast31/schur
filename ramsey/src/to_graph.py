import sys
import numpy as np


def load_partition(filename):
    with open(filename) as file:
        lines = file.readlines()
    partition = []
    for i, line in enumerate(lines, 1):
        for x in map(int, line.split()):
            delta = x - len(partition)
            if delta > 0:
                partition.extend([0] * delta)
            partition[x - 1] = i
    return partition


def to_graph(partition):
    size = len(partition) + 1
    graph = np.zeros((size, size), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            x = abs(i - j)
            color = partition[x - 1]
            graph[i, j] = color
    return graph


def main():
    partition_file = sys.argv[1]
    partition = load_partition(partition_file)
    graph = to_graph(partition)
    try:
        file = partition_file.split('/')[3]
    except IndexError:
        file = partition_file.split('\\')[3]
    caracs = file[2:-5]
    cliques, size = caracs.split(';')
    filename = f"../results/graphs/R({cliques};{int(size) + 1}).npy"
    np.save(filename, graph)


if __name__ == '__main__':
    main()
