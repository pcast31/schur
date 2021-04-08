from utils import break_symmetries, disjoint, use_all, weakly_sum_free, load_pos


def search_space(k, n):
    cnf = load_pos(6, "possibilities/5.txt")
    for i in range(210, 350):
        cnf.append(f"{k * (i - 1) + 6}")
    return cnf


def weak_schur_cnf(k, n):
    cnf = weakly_sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(disjoint(k, n))
    cnf.extend(break_symmetries(k))
    cnf.extend(search_space(k, n))
    return cnf


def weak_schur_dimacs(k, n):
    cnf = weak_schur_cnf(k, n)
    print(f"p cnf {k * n} {len(cnf)}")
    print(*cnf, sep=" 0\n", end=" 0\n")


if __name__ == "__main__":
    k = 6
    n = 583
    weak_schur_dimacs(k, n)
