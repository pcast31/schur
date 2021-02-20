def weakly_sum_free(k, n):
    cnf = []
    for c in range(k):
        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                tot = a + b
                if tot <= n:
                    no_sum = f"-{a * k - c} -{b * k - c} -{tot * k - c}"
                    cnf.append(no_sum)
    return cnf


def use_all(k, n):
    cnf = []
    for i in range(n):
        use_i = " ".join(map(str, range(k * i + 1, k * (i + 1) + 1)))
        cnf.append(use_i)
    return cnf


def search_space(k, partition):
    cnf = ["1", str(k + 1)]
    for i, color in enumerate(partition):
        for n in color:
            for a in (4 * n, 4 * n + 1):
                cnf.append(str(k * (a - 1) + 2 + i))
            for a in (4 * n - 1, 4 * n + 2):
                cnf.append(f"{k * (a - 1) + 2 + i} {k * (a - 1) + 1}")
    return cnf


def to_cnf(k, n, partition):
    cnf = weakly_sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(search_space(k, partition))
    return cnf


def encode_dimacs(k, n, partition):
    cnf = to_cnf(k, n, partition)
    return f"p cnf {k * n} {len(cnf)}\n" + " 0\n".join(cnf) + " 0\n"
