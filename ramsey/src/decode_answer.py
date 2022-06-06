import sys


def decode_answer(k, n):
    is_var_line = lambda line: line[0] == 'v'
    trim_line = lambda line: line[2:].rstrip('\n 0')

    solution = filter(is_var_line, sys.stdin.readlines())
    solution = map(trim_line, solution)
    solution = " ".join(solution).split()
    solution = map(int, solution)

    assigned = set()
    solu = {}
    prev = 0
    for x in solution:
        prev += 1
        if x <= 0:
            continue
        if x < prev:
            x *= 10
        x -= 1
        i, colour = divmod(x, k)
        number = i + 1
        if number not in assigned:
            assigned.add(number)
            solu[number] = colour
        else:
            raise RuntimeError
    assert assigned == set(range(1, n + 1))

    partition = [[] for _ in range(k)]
    for i in range(1, n + 1):
        partition[solu[i]].append(i)

    return partition


def main():
    k = int(sys.argv[1])
    n = int(sys.argv[2])
    partition = decode_answer(k, n)
    for col in partition:
        print(*col)


if __name__ == '__main__':
    main()
