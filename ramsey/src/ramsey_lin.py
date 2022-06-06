import itertools
import sys


def not_a_clique(n_colors, color, subset):
    clause = []
    for x, y in itertools.combinations(subset, 2):
        z = abs(y - x)
        lit = n_colors * (z - 1) + color
        clause.append(-lit)
    for x in subset:
        lit = n_colors * (x - 1) + color
        clause.append(-lit)
    clause = " ".join(map(str, clause))
    return clause


def no_clique(n_colors, maxi, color, size):
    cnf = []
    for subset in itertools.combinations(range(1, maxi + 1), size - 1):
        clause = not_a_clique(n_colors, color, subset)
        cnf.append(clause)
    return cnf


def use_all(n_colors, maxi):
    cnf = []
    for x in range(1, maxi + 1):
        use_x = " ".join(map(str, range(n_colors * (x - 1) + 1, n_colors * x + 1)))
        cnf.append(use_x)
    return cnf


def disjoint(n_colors, maxi):
    cnf = []
    for c_1 in range(n_colors):
        for c_2 in range(c_1 + 1, n_colors):
            for x in range(1, maxi + 1):
                lit_1 = n_colors * x - c_1
                lit_2 = n_colors * x - c_2
                not_both = f"-{lit_1} -{lit_2}"
                cnf.append(not_both)
    return cnf


def order_colors(n_colors, maxi):
    cnf = ["1"]
    for color in range(3, n_colors + 1):
        clause = ""
        for x in range(1, maxi + 1):
            lit = n_colors * (x - 1) + color
            ordered = clause + str(-lit)
            cnf.append(ordered)
            lit = n_colors * (x - 1) + color - 1
            clause += f"{lit} "
    return cnf


def ram_lin_cnf(maxi, clique_sizes, order):
    n_colors = len(clique_sizes)
    cnf = []
    for color, size in enumerate(clique_sizes, 1):
        cnf.extend(no_clique(n_colors, maxi, color, size))
    cnf.extend(use_all(n_colors, maxi))
    cnf.extend(disjoint(n_colors, maxi))
    if order:
        cnf.extend(order_colors(n_colors, maxi))
    return cnf


def ram_lin_dimacs(maxi, clique_sizes, order):
    n_colors = len(clique_sizes)
    cnf = ram_lin_cnf(maxi, clique_sizes, order)
    header = f"p cnf {n_colors * maxi} {len(cnf)}\n"
    dimacs = header + " 0\n".join(cnf) + " 0\n"
    return dimacs


def main():
    clique_sizes = list(map(int, sys.argv[1].split(',')))
    maxi = int(sys.argv[2])
    try:
        order = sys.argv[3] == "--order"
    except IndexError:
        order = False
    dimacs = ram_lin_dimacs(maxi, clique_sizes, order)
    print(dimacs)


if __name__ == "__main__":
    main()
