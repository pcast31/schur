from sys import argv


def max_len(k, n, d):
    cnf = []
    for c in range(k):
        for i in range(1, d + 1):
            for j in range(d + 1, n + d + 1):
                tot = i + j
                if tot > n + d:
                    break
                no_sum = f"-{i * k - c} -{j * k - c} -{tot * k - c}"
                cnf.append(no_sum)
    return cnf


def weakly_sum_free(k, n):
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
        for i in range(2, 9):
            cnf.append(clause + f"-{k * i + 4}")
            clause += f"{k * i + 3} "
    if k >= 5:
        clause= ""
        for i in range(2, 24):
            cnf.append(clause + f"-{k * i + 5}")
            clause += f"{k * i + 4} "
    if k >= 6:
        clause= ""
        for i in range(2, 67):
            cnf.append(clause + f"-{k * i + 6}")
            clause += f"{k * i + 5} "
    return cnf


def weak_schur_cnf(k, n, d):
    cnf = []
    cnf.extend(weakly_sum_free(k, d))
    cnf.extend(use_all(k, n + d))
    cnf.extend(disjoint(k, n + d))
    cnf.extend(break_symmetries(k))
    cnf.extend(max_len(k, n, d))
    return cnf


def weak_schur_dimacs(k, n, d):
    cnf = weak_schur_cnf(k, n, d)
    print(f"p cnf {k * (n + d)} {len(cnf)}")
    print(*cnf, sep=" 0\n", end=" 0\n")


if __name__ == "__main__":
    k = 3
    n = int(argv[1])
    d = int(argv[2])
    weak_schur_dimacs(k, n, d)
