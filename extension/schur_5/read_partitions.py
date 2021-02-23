import pickle


def read_partitions():
    with open("partitions", 'rb') as file:
        partitions = pickle.load(file)
    return partitions
