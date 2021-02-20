import os
import subprocess
import tqdm

from encode_dimacs import encode_dimacs
from decode_answer import decode_answer


def save_partition(partition, filename):
    with open("../extended/" + filename, "w") as file:
        for colour in partition:
            file.write(" ".join(map(str, colour)) + "\n")


def main(filename):
    partition = []
    with open("../partitions/" + filename) as file:
        for color in file.readlines():
            color = color.strip()
            partition.append(list(map(int, color.split())))

    dimacs = encode_dimacs(5, 179, partition).encode('utf-8')
    cmd = "./solvers/lingeling/plingeling"
    result = subprocess.run(cmd, stdout=subprocess.PIPE, input=dimacs)
    partition = decode_answer(5, result.stdout.decode('utf-8'))

    if partition is None:
        return False
    save_partition(partition, filename)
    return True


if __name__ == '__main__':
    count = 0
    _, _, partitions = next(os.walk("../partitions"))

    for filename in tqdm.tqdm(partitions):
        if main(filename):
            count += 1

    print(f"Successfully extended {count} partitions out of {len(partitions)}.")
