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


def weak_schur_4(k, n):
    cnf = []
    cnf.extend(list(str(k * i + c) for i, c in enumerate(
        [1, 1, 2, 1, 2, 2, 2, 1, 3, 3, 1, 3, 3, 3, 3])))
    cnf.append(f"{k * 15 + 1} {k * 15 + 3}")
    cnf.extend(list(str(k * (i + 16) + c) for i, c in enumerate(
        [3, 3, 2, 3, 2, 1, 2, 4, 1, 4, 4, 4, 4, 4])))
    cnf.append(f"{k * 30 + 1} {k * 30 + 4}")
    cnf.append(f"{k * 31 + 1} {k * 31 + 4}")
    cnf.append(str(k * 32 + 4))
    cnf.append(f"{k * 33 + 1} {k * 33 + 2} {k * 33 + 4}")
    cnf.append(f"{k * 34 + 1} {k * 34 + 2} {k * 34 + 4}")
    cnf.append(f"{k * 35 + 2} {k * 35 + 4}")
    cnf.append(f"{k * 36 + 1} {k * 36 + 2} {k * 36 + 4}")
    cnf.append(f"{k * 37 + 1} {k * 37 + 2} {k * 37 + 4}")
    cnf.append(f"{k * 38 + 1} {k * 38 + 2} {k * 38 + 4}")
    cnf.append(f"{k * 39 + 1} {k * 39 + 4}")
    cnf.append(str(k * 40 + 4))
    cnf.append(str(k * 41 + 4))
    cnf.append(f"{k * 42 + 1} {k * 42 + 4}")
    cnf.append(f"{k * 43 + 1} {k * 43 + 4}")
    cnf.append(f"{k * 44 + 1} {k * 44 + 4}")
    cnf.append(f"{k * 45 + 1} {k * 45 + 4}")
    cnf.append(str(k * 46 + 4))
    cnf.append(f"{k * 47 + 1} {k * 47 + 4}")
    cnf.append(str(k * 48 + 4))
    cnf.append(f"{k * 49 + 1} {k * 49 + 2}")
    cnf.append(str(k * 50 + 2))
    cnf.append(str(k * 51 + 2))
    cnf.append(f"{k * 52 + 1} {k * 52 + 2}")
    cnf.append(str(k * 53 + 3))
    cnf.append(str(k * 54 + 3))
    cnf.append(f"{k * 55 + 1} {k * 55 + 3}")
    cnf.append(f"{k * 56 + 1} {k * 56 + 3}")
    cnf.append(f"{k * 57 + 1} {k * 57 + 3}")
    cnf.append(f"{k * 58 + 1} {k * 58 + 3}")
    cnf.append(f"{k * 59 + 1} {k * 59 + 3}")
    cnf.append(str(k * 60 + 3))
    cnf.append(str(k * 61 + 3))
    cnf.append(f"{k * 62 + 1} {k * 62 + 2}")
    cnf.append(str(k * 63 + 2))
    cnf.append(str(k * 64 + 2))
    cnf.append(f"{k * 65 + 1} {k * 65 + 2}")
    return cnf


def search_space(k, n):
    cnf = weak_schur_4(k, n)

    for i in range(25, 67):
        cnf.append(f"-{k * (i - 1) + 5}")
    cnf.append(str(k * 66 + 5))

    if k >= 6:
        for i in range(25, 187):
            cnf.append(f"-{k * (i - 1) + 6}")
        for i in range(220, 320):
            cnf.append(str(k * (i - 1) + 6))
    return cnf


def schur_cnf(k, n):
    cnf = sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(search_space(k, n))
    return cnf


def schur_dimacs(k, n):
    cnf = schur_cnf(k, n)
    print(f"p cnf {k * n} {len(cnf)}")
    print(*cnf, sep=" 0\n", end=" 0\n")


if __name__ == "__main__":
    k = int(argv[1])
    n = int(argv[2])
    schur_dimacs(k, n)
