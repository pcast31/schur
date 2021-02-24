import argparse
import pickle


def main(seeds, stop=None):
    if stop is None:
        stop = 3 * 10 ** 9

    stack = seeds.copy()
    partitions = set(seeds)
    i = 0

    while stack:
        partition = stack.pop()
        for neighbour in neighbours(partition):
            if neighbour not in partitions:
                partitions.add(neighbour)
                stack.append(neighbour)

        i += 1
        if i % 10_000 == 0:
            print("partitions found : {} -- nodes in stack : {}".format(
                len(partitions), len(stack)
            ))
        if len(partitions) >= stop:
            break

    print("\n", len(partitions), " partitions found", sep="")
    save_partitions(partitions)


def save_partitions(partitions):
    partitions = sorted(partitions, reverse=True)
    with open("partitions", 'wb') as file:
        pickle.dump(partitions, file)


def neighbours(partition):
    subsets, word, mins = from_int(partition)
    for i, subset in enumerate(subsets):
        choices = set(range(1, 161))
        choices.difference_update(compute_forbidden(subset))

        for n in choices:
            j = word[n]
            if j != 4 and n == mins[j][0] and (i > j or mins[j][1] > mins[j + 1][0]):
                yield reorder(word, n, i)
            else:
                yield partition + (i - j) * (5 ** n)


def reorder(word, n, i):
    j = word[n]
    word[n] = i

    order = [None] * 5
    count = 0
    for p in range(1, 161):
        k = word[p]
        if order[k] is None:
            order[k] = count
            if count == 4:
                break
            count += 1

    pow_5 = 1
    acc = 0
    for p in range(1, 161):
        pow_5 *= 5
        acc += order[word[p]] * pow_5

    word[n] = j
    return acc


def compute_forbidden(subset):
    forbidden = set(subset)
    for i, a in enumerate(subset):
        if a % 2 == 0:
            forbidden.add(a // 2)
        for j in range(i):
            forbidden.add(a - subset[j])
        for j in range(i, len(subset)):
            tot = a + subset[j]
            if tot > 160:
                break
            forbidden.add(tot)
    return forbidden


def from_int(partition):
    subsets = [[] for _ in range(5)]
    word = [None] * 161
    mins = [[] for _ in range(5)]

    for n in range(1, 161):
        partition //= 5
        i = partition % 5
        subsets[i].append(n)
        word[n] = i
        mini = mins[i]
        if len(mini) < 2:
            mini.append(n)

    return subsets, word, mins


def to_int(partition):
    num = 0
    for i, subset in enumerate(partition):
        num += i * sum(5 ** n for n in subset)
    return num


A_HEULE = {1, 4, 9, 11, 14, 16, 19, 21, 29, 31, 34, 39, 49, 51, 54, 57, 64, 69,
           77, 84, 92, 97, 104, 107, 110, 112, 122, 127, 130, 132, 140, 142,
           145, 147, 150, 152, 157, 160}

B_HEULE = {2, 3, 12, 13, 30, 38, 44, 48, 52, 53, 58, 62, 63, 72, 80, 81, 89, 98,
           99, 103, 108, 109, 113, 117, 123, 131, 148, 149, 158, 159}

C_HEULE = {5, 6, 7, 8, 18, 20, 33, 35, 37, 46, 47, 50, 59, 60, 71, 73, 75, 86,
           88, 90, 101, 102, 111, 114, 115, 124, 126, 128, 141, 143, 153, 154,
           155, 156}

D_HEULE = {10, 17, 22, 40, 41, 42, 43, 55, 56, 61, 67, 68, 70, 91, 93, 94, 100,
           105, 106, 118, 119, 120, 121, 139, 144, 151}

E_HEULE = {15, 23, 24, 25, 26, 27, 28, 32, 36, 45, 65, 66, 74, 76, 78, 79, 82,
           83, 85, 87, 95, 96, 116, 125, 129, 133, 134, 135, 136, 137, 138, 146}

HEULE = [A_HEULE, B_HEULE, C_HEULE, D_HEULE, E_HEULE]


A_EXOO = {1, 6, 10, 18, 21, 23, 26, 30, 34, 38, 43, 45, 50, 54, 65, 74}

B_EXOO = {2, 3, 8, 14, 19, 20, 24, 25, 36, 46, 47, 51, 62, 73}

C_EXOO = {4, 5, 15, 16, 22, 28, 29, 39, 40, 41, 42, 48, 49, 59}

D_EXOO = {7, 9, 11, 12, 13, 17, 27, 31, 32, 33, 35, 37, 53, 56, 57, 61, 79}

E_EXOO = {44, 52, 55, 58, 60, 63, 64, 66, 67, 68, 69, 70, 71, 72, 75, 76, 77,
          78, 80}

EXOO = [A_EXOO, B_EXOO, C_EXOO, D_EXOO, E_EXOO]

for subset in EXOO:
    subset_copy = subset.copy()
    for i in subset_copy:
        subset.add(161 - i)


PARTITIONS = [to_int(HEULE), to_int(EXOO)]


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="test setup")
    args.add_argument('--stop', type=int)
    args = args.parse_args()

    main(PARTITIONS, args.stop)
