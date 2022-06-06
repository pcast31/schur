import itertools
import subprocess
import sys

import tqdm


def parse_clique_sizes(text):
    sizes = text.split(',')
    try:
        spec_col = sizes.index('t') + 1
    except ValueError as err:
        raise ValueError("Template color should be desginated as 't'.") from err
    sizes[spec_col - 1] = '3'
    sizes = list(map(int, sizes))
    return sizes, spec_col


def cart_tups(width, head, subset):
    tups = [subset[0]]
    for x in subset[1:]:
        if x < tups[-1]:
            if x > head:
                while x < tups[-1]:
                    x += width
                tups.append(x)
            else:
                return None
        else:
            tups.append(x)
    return tups


def mr_tree(width, head, subset):
    if len(subset) <= 1:
        yield subset
        return
    x = subset[0]
    y = subset[1]
    for mod_subset in mr_tree(width, head, subset[1:]):
        yield [x] + mod_subset
        if y > head and y - x <= head:
            yield [x] + [z + width for z in mod_subset]


def graph_diffs(width, head, subset):
    diffs = [projection(width, head, x) for x in subset]
    for i, x in enumerate(subset[:-1], 1):
        for y in subset[i:]:
            z = projection(width, head, y - x)
            diffs.append(z)
    return diffs


def projection(width, head, x):
    if x > head:
        x %= width
        if x <= head:
            x += width
    return x


def tf_spec(n_colors, width, head, spec_col):
    cnf = [f"{n_colors * (width - 1) + spec_col}"]
    maxi = width + head
    for x in range(1, maxi + 1):
        for y in range(x, maxi + 1):
            z = x + y
            if maxi < z <= maxi + width:
                continue
            z = projection(width, head, z)
            lit_x = n_colors * (x - 1) + spec_col
            lit_y = n_colors * (y - 1) + spec_col
            lit_z = n_colors * (z - 1) + spec_col
            no_sum = f"-{lit_x} -{lit_y} -{lit_z}"
            cnf.append(no_sum)
    return cnf


def not_a_clique(n_colors, color, subset):
    clause = []
    for x in subset:
        lit = n_colors * (x - 1) + color
        clause.append(-lit)
    clause = " ".join(map(str, clause))
    return clause


def no_clique(n_colors, width, head, color, size):
    maxi = width + head
    cnf = []
    for subset in itertools.permutations(range(1, maxi + 1), size - 1):
        prod_subsets = cart_tups(width, head, subset)
        if prod_subsets is None:
            continue
        for mod_subset in mr_tree(width, head, prod_subsets):
            diffs = graph_diffs(width, head, mod_subset)
            clause = not_a_clique(n_colors, color, diffs)
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


def tf_template_cnf(width, head, clique_sizes, spec_col, order):
    n_colors = len(clique_sizes)
    maxi = width + head
    cnf = []
    for color, size in enumerate(clique_sizes, 1):
        if color == spec_col:
            cnf.extend(tf_spec(n_colors, width, head, spec_col))
        else:
            cnf.extend(no_clique(n_colors, width, head, color, size))
    cnf.extend(use_all(n_colors, maxi))
    cnf.extend(disjoint(n_colors, maxi))
    if order:
        cnf.extend(order_colors(n_colors, maxi))
    return cnf


def tf_template_dimacs(width, head, clique_sizes, spec_col, order):
    n_colors = len(clique_sizes)
    maxi = width + head
    cnf = tf_template_cnf(width, head, clique_sizes, spec_col, order)
    header = f"p cnf {n_colors * maxi} {len(cnf)}\n"
    dimacs = header + " 0\n".join(cnf) + " 0\n"
    return dimacs


def is_solution(answer):
    for line in answer.splitlines():
        if line[0] != 's':
            continue
        return line[2] == 'S'
    raise RuntimeError


def auto_search(clique_sizes, spec_col, max_size, min_width, order):
    cmd = ["../solvers/lingeling/plingeling", '-n']
    for width in range(min_width, max_size + 1):
        print()
        print(width)
        for head in tqdm.trange(max_size - width, -1, -1):
            dimacs = tf_template_dimacs(width, head, clique_sizes, spec_col, order)
            dimacs = dimacs.encode('utf-8')
            result = subprocess.run(cmd, stdout=subprocess.PIPE, input=dimacs)
            if is_solution(result.stdout.decode('utf-8')):
                break
        else:
            continue
        print(f"\n{width} -- {head}\n")


def main():
    if sys.argv[1] == "--auto":
        clique_sizes, spec_col = parse_clique_sizes(sys.argv[2])
        max_size = int(sys.argv[3])
        min_width = int(sys.argv[4])
        try:
            order = sys.argv[5] == "--order"
        except IndexError:
            order = False
        auto_search(clique_sizes, spec_col, max_size, min_width, order)
    else:
        clique_sizes, spec_col = parse_clique_sizes(sys.argv[1])
        width = int(sys.argv[2])
        head = int(sys.argv[3])
        try:
            order = sys.argv[4] == "--order"
        except IndexError:
            order = False
        dimacs = tf_template_dimacs(width, head, clique_sizes, spec_col, order)
        print(dimacs)


if __name__ == "__main__":
    main()
