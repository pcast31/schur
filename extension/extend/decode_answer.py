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


def decode_answer(k, solution):
    is_var_line = lambda line: line[0] == 'v'
    trim_line = lambda line: line[2:].rstrip('\n 0')

    solution = filter(is_var_line, solution.splitlines())
    solution = map(trim_line, solution)
    solution = " ".join(solution).split()
    solution = map(int, solution)

    assigned = set()
    partition = [[] for _ in range(k)]

    for x in solution:
        if x <= 0:
            continue
        x -= 1
        n, colour = divmod(x, k)
        number = n + 1
        if number not in assigned:
            partition[colour].append(number)
            assigned.add(number)

    if 1 not in assigned:
        return None
    return partition
