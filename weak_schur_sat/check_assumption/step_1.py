'''
Checks wether there exists a weak schue partition of 1..n in 4 subsets
satisfying the given constraints.

Put the constraints in the constraints function.

step_1 n [mode]
'''

from sys import argv
from utils import break_symmetries, disjoint, use_all, weakly_sum_free


def constraints_66():
    cnf = [" ".join(map(str, range(4, 4 * 23 + 1, 4)))]
    return cnf


def constraints_65():
    try:
        mode = argv[2]
    except IndexError:
        mode = None

    if mode == 'lowlim':
        cnf = [" ".join(map(str, range(4, 4 * 22 + 1, 4)))]
        return cnf

    cnf = [" ".join(map(str, range(3, 4 * 7 + 4, 4)))]
    for i in range(1, 23):
        cnf.append(f"-{4 * i}")
    cnf.append(f"{4 * 23}")
    return cnf


def constraints(n):
    if n == 66:
        return constraints_66()
    if n == 65:
        return constraints_65()
    # example
    cnf = ["-4", "-8", "-12", "-16", "-20", "-24", "-28", "-32", "-36", "-40",
           "-44", "-48", "52"]
    return cnf


def weak_schur_cnf(k, n):
    cnf = weakly_sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(disjoint(k, n))
    cnf.extend(break_symmetries(k))
    cnf.extend(constraints(n))
    return cnf


def weak_schur_dimacs(k, n):
    cnf = weak_schur_cnf(k, n)
    print(f"p cnf {k * n} {len(cnf)}")
    print(*cnf, sep=" 0\n", end=" 0\n")


if __name__ == "__main__":
    k = 4
    n = int(argv[1])
    weak_schur_dimacs(k, n)
