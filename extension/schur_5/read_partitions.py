import pickle


def from_int(int_repr):
    partition = [[] for _ in range(5)]
    for n in range(1, 161):
        int_repr //= 5
        i = int_repr % 5
        partition[i].append(n)
    return partition


def read_partitions():
    with open("partitions", 'rb') as file:
        int_reprs = pickle.load(file)
    partitions = []
    for int_repr in int_reprs:
        partition = from_int(int_repr)
        partitions.append(partition)
    return partitions
