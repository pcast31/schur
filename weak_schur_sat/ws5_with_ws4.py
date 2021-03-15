from sys import argv


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


def search_space(n):
    cnf = []
    cnf.extend(list(str(5 * i + c) for i, c in enumerate(
        [1, 1, 2, 1, 2, 2, 2, 1, 3, 3, 1, 3, 3, 3, 3])))
    cnf.extend([f"{5 * 16 - 4} {5 * 16 - 2}", f"{5 * 17 - 4} {5 * 17 - 2}"])
    cnf.extend(list(str(5 * (i + 17) + c) for i, c in enumerate(
        [3, 2, 3, 2, 1, 2, 4])))
    for i in range(25, 67):
        cnf.append(str(-5 * i))
    cnf.append(str(5 * 67))
    return cnf


def schur_cnf(k, n):
    cnf = sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(search_space(n))
    return cnf


def schur_dimacs(k, n):
    cnf = schur_cnf(k, n)
    print(f"p cnf {k * n} {len(cnf)}")
    print(*cnf, sep=" 0\n", end=" 0\n")


if __name__ == "__main__":
    k = 5
    n = int(argv[1])
    schur_dimacs(k, n)
