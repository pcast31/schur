import sys


def build_mapping(n, lim):
    mapping = {1: 1, 2: 2}
    count = 2
    for a in range(3, min(4 * lim + 3, n + 1)):
        if a % 4 != 1:
            count += 1
        mapping[a] = count
    for a in range(4 * lim + 3, n + 1):
        count += 1
        mapping[a] = count
    return mapping, count


def is_sum_free(s_raw):
    s_list = list(s_raw)
    s_set = set(s_raw)

    for i, a in enumerate(s_list):
        for j in range(i + 1, len(s_list)):
            b = s_list[j]
            if a + b in s_set:
                print(a, b, a + b)
                return False
    return True


def decode_answer(n, mapping, count):
    is_var_line = lambda line: line[0] == 'v'
    trim_line = lambda line: line[2:].rstrip('\n 0')

    solution = filter(is_var_line, sys.stdin.readlines())
    solution = map(trim_line, solution)
    solution = " ".join(solution).split()
    solution = map(int, solution)

    assigned = set()
    solu = {}
    for x in solution:
        if x <= 0:
            continue
        x -= 1
        i, colour = divmod(x, 6)
        number = i + 1
        if number not in assigned:
            assigned.add(number)
            solu[number] = colour
        else:
            raise RuntimeError
    assert assigned == set(range(1, count + 1))

    partition = [[] for _ in range(6)]
    for i in range(1, n + 1):
        j = mapping[i]
        partition[solu[j]].append(i)

    assert all(map(is_sum_free, partition))
    return partition


def main():
    n = int(sys.argv[1])
    lim = int(sys.argv[2])
    mapping, count = build_mapping(n, lim)
    partition = decode_answer(n, mapping, count)
    for col in partition:
        print(*col)


if __name__ == '__main__':
    main()
