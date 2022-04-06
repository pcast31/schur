import subprocess
import sys
import tqdm


def sum_free(n):
    cnf = []
    for c in range(5):
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                tot = i + j
                if tot > n:
                    break
                x = 5 * i
                y = 5 * j
                z = 5 * tot
                no_sum = f"-{x  - c} -{y - c} -{z - c}"
                cnf.append(no_sum)
    return cnf


def template_constraints(n):
    cnf = []
    for c in range(1, 5):
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                tot = i + j - n
                if tot <= 0:
                    continue
                x = 5 * i
                y = 5 * j
                z = 5 * tot
                no_sum_mod = f"-{x - c} -{y - c} -{z - c}"
                cnf.append(no_sum_mod)
    return cnf


def use_all(n):
    cnf = []
    for i in range(n):
        use_i = " ".join(map(str, range(5 * i + 1, 5 * (i + 1) + 1)))
        cnf.append(use_i)
    return cnf


def disjoint(n):
    cnf = []
    for i in range(1, n + 1):
        for c1 in range(5):
            for c2 in range(c1 + 1, 5):
                not_both = f"-{5 * i - c1} -{5 * i - c2}"
                cnf.append(not_both)
    return cnf


def apply_backdoor(lim, backdoor_num):
    filename = f"backdoors/backdoor-{backdoor_num}"
    cnf = []
    with open(filename) as file:
        lines = file.readlines()[:lim]
    for a, possibilities in enumerate(lines):
        to_litterals = lambda c: str(5 * a + int(c))
        clause = ' '.join(map(to_litterals, possibilities.split()))
        cnf.append(clause)
    return cnf


def s_template_cnf(n, lim, backdoor):
    cnf = []
    cnf.extend(sum_free(n))
    cnf.extend(template_constraints(n))
    cnf.extend(use_all(n))
    cnf.extend(disjoint(n))
    cnf.extend(apply_backdoor(lim, backdoor))
    return cnf


def s_template_dimacs(n, lim, backdoor):
    cnf = s_template_cnf(n, lim, backdoor)
    return f"p cnf {5 * n} {len(cnf)}\n" + " 0\n".join(cnf) + " 0\n"


def is_solution(answer):
    for line in answer.splitlines():
        if line[0] != 's':
            continue
        return line[2] == 'S'
    raise RuntimeError


def main():
    n = int(sys.argv[1])
    lim = int(sys.argv[2])
    try:
        backdoor = int(sys.argv[3])
        dimacs = s_template_dimacs(n, lim, backdoor)
        print(dimacs)
    except IndexError:
        #bonne valeurs : n = 118 -- lim = 20
        cmd = ["./solvers/lingeling/plingeling", '-n']
        backdoors = range(1, 1617):
        #backdoors = [170, 257, 258, 259, 260, 261, 953, 954, 955, 956, 1129]
        for backdoor in tqdm.tqdm(backdoors):
            dimacs =s_template_dimacs(n, lim, backdoor)
            dimacs = dimacs.encode('utf-8')
            result = subprocess.run(cmd, stdout=subprocess.PIPE, input=dimacs)
            if is_solution(result.stdout.decode('utf-8')):
                print(f"\n\n\n{backdoor}\n\n\n")

if __name__ == '__main__':
    main()
