from sys import argv


def get_max_len(m_4):
    if m_4 >= 22:
        return 17
    if m_4 >= 10:
        return 18
    if m_4 == 9:
        return 21
    return None


def load_pos(k, file):
    cnf = []
    with open(file) as f:
        for i, line in enumerate(f.readlines()):
            clause = ""
            for c in map(int, line.strip().split()):
                clause += f"{k * i + c} "
            cnf.append(clause[:-1])
    return cnf


def sum_free(k, n):
    cnf = []
    for c in range(k):
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                tot = i + j
                if tot > n:
                    break
                no_sum = f"-{i * k - c} -{j * k - c} -{tot * k - c}"
                cnf.append(no_sum)
    return cnf


def use_all(k, n):
    cnf = []
    for i in range(n):
        use_i = " ".join(map(str, range(k * i + 1, k * (i + 1) + 1)))
        cnf.append(use_i)
    return cnf


def disjoint(k, n):
    cnf = []
    for i in range(1, n + 1):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append(f"-{k * i - c1} -{k * i - c2}")
    return cnf


def break_symmetries(k):
    cnf = ["1"]
    if k >= 3:
        cnf.append(f"-{k + 3}")
        cnf.append(f"{k + 2} -{2 * k + 3}")
    if k >= 4:
        clause= ""
        for i in range(1, 9):
            cnf.append(clause + f"-{k * i + 4}")
            clause += f"{k * i + 3} "
    if k >= 5:
        clause= ""
        for i in range(1, 24):
            cnf.append(clause + f"-{k * i + 5}")
            clause += f"{k * i + 4} "
    if k >= 6:
        clause= ""
        for i in range(1, 67):
            cnf.append(clause + f"-{k * i + 6}")
            clause += f"{k * i + 5} "
    return cnf


def search_space(n, m_4, lim):
    try:
        cnf = load_pos(5, "sghts")
    except FileNotFoundError:
        cnf = []

    for i in range(m_4 - 1):
        cnf.append(f"-{5 * i + 4}")
    cnf.append(f"{k * (m_4 - 1) + 4}")
    for i in range(1, lim):
        cnf.append(f"-{5 * i}")

    max_len = get_max_len(m_4)
    if max_len is not None:
        for i in range(m_4, n - max_len + 1):
            clause = ""
            for j in range(i, i + max_len + 1):
                clause += f"{5 * j - 1} {5 * j} "
            cnf.append(clause[:-1])

    return cnf


def schur_cnf(k, n, m_4, lim):
    cnf = sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(disjoint(k, n))
    cnf.extend(break_symmetries(k))
    cnf.extend(search_space(n, m_4, lim))
    return cnf


def schur_dimacs(k, n, m_4, lim):
    cnf = schur_cnf(k, n, m_4, lim)
    print(f"p cnf {k * n} {len(cnf)}")
    print(*cnf, sep=" 0\n", end=" 0\n")


if __name__ == "__main__":
    k = 5
    n = int(argv[1])
    m_4 = int(argv[2])
    lim = int(argv[3])
    schur_dimacs(k, n, m_4, lim)
