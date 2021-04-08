'''
Finds every color in which can be the numbers in 1..65 if k = 4 and in 1..185
if k = 5.
'''

import subprocess
import sys
import tqdm

from utils import break_symmetries, disjoint, use_all, weakly_sum_free, load_pos


def is_solution(answer):
    for line in answer.splitlines():
        if line[0] != 's':
            continue
        return line[2] == 'S'
    raise RuntimeError


def search_space_4(k, n, i, c_i):
    cnf = ["1", f"{k + 1}", f"{2 * k + 2}", f"{3 * k + 1}", f"{4 * k + 2}",
           f"{5 * k + 2}", f"{6 * k + 2}", f"{7 * k + 1}", f"{8 * k + 3}"]
    cnf.extend(map(str, range(-k, -(21 * k + 5), -k)))
    cnf.append(f"{k * 22 + 4} {k * 23 + 4}")
    cnf.append(f"{k * (i - 1) + c_i}")
    return cnf


def search_space_5(k, n, i, c_i, pos_start):
    cnf = pos_start.copy()
    cnf.append(f"{k * (i - 1) + c_i}")
    return cnf


def search_space(k, n, i, c_i, pos_start):
    if k == 4:
        return search_space_4(k, n, i, c_i)
    if k == 5:
        return search_space_5(k, n, i, c_i, pos_start)
    raise ValueError


def weak_schur_cnf(k, n, i, c_i, pos_start):
    cnf = weakly_sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(disjoint(k, n))
    cnf.extend(break_symmetries(k))
    cnf.extend(search_space(k, n, i, c_i, pos_start))
    return cnf


def weak_schur_dimacs(k, n, i, c_i, pos_start):
    cnf = weak_schur_cnf(k, n, i, c_i, pos_start)
    text = f"p cnf {k * n} {len(cnf)}\n" + " 0\n".join(cnf) + " 0\n"
    return text


def main():
    k = int(sys.argv[1])
    if k == 4:
        n = 65
        pos_start = None
    elif k == 5:
        n = 185
        pos_start = load_pos(5, "possibilities/4.txt")
    else:
        raise ValueError
    pos = []

    for i in tqdm.tqdm(range(1, n + 1)):
        pos.append([])
        for c_i in range(1, k + 1):
            dimacs = weak_schur_dimacs(k, n, i, c_i, pos_start).encode('utf-8')
            cmd = ["../solvers/lingeling/plingeling", '-n']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, input=dimacs)
            if is_solution(result.stdout.decode('utf-8')):
                pos[-1].append(c_i)

    print()
    for p in pos:
        print(*p)


if __name__ == "__main__":
    main()
