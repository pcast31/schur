import subprocess
import sys
import tqdm


def build_mapping(n, lim):
    mapping = {1: 1, 2: 2}
    count = 2
    for a in range(3, min(4 * lim + 3, n + 1)):
        if a % 4 != 1:
            count += 1
        mapping[a] = count
    for a in range(4 * lim + 3, n + 1):
        count += 1
        mapping[a] = count
    return mapping, count


def weakly_sum_free(n, mapping):
    cnf = []
    for c in range(6):
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                tot = i + j
                if tot > n:
                    break
                x = 6 * mapping[i]
                y = 6 * mapping[j]
                z = 6 * mapping[tot]
                no_sum = f"-{x  - c} -{y - c} -{z - c}"
                cnf.append(no_sum)
    return cnf


def use_all(count):
    cnf = []
    for i in range(count):
        use_i = " ".join(map(str, range(6 * i + 1, 6 * (i + 1) + 1)))
        cnf.append(use_i)
    return cnf


def disjoint(count):
    cnf = []
    for i in range(1, count + 1):
        for c1 in range(6):
            for c2 in range(c1 + 1, 6):
                cnf.append(f"-{6 * i - c1} -{6 * i - c2}")
    return cnf


def apply_backdoor(mapping, lim, backdoor_num):
    filename = f"backdoors/backdoor-{backdoor_num}"
    cnf = ["1", "7"]
    with open(filename) as file:
        for a, possibilities in enumerate(file.readlines()[:lim]):
            base_lit = mapping[4 * (a + 1)]
            to_litterals = lambda c: str(6 * (base_lit - 1) + int(c) + 1)
            clause = ' '.join(map(to_litterals, possibilities.split()))
            cnf.append(clause)
    return cnf


def weak_schur_cnf(n, mapping, count, lim, backdoor):
    cnf = weakly_sum_free(n, mapping)
    cnf.extend(use_all(count))
    cnf.extend(disjoint(count))
    cnf.extend(apply_backdoor(mapping, lim, backdoor))
    return cnf


def weak_schur_dimacs(n, mapping, count, lim, backdoor):
    cnf = weak_schur_cnf(n, mapping, count, lim, backdoor)
    return f"p cnf {6 * count} {len(cnf)}\n" + " 0\n".join(cnf) + " 0\n"


def is_solution(answer):
    for line in answer.splitlines():
        if line[0] != 's':
            continue
        return line[2] == 'S'
    raise RuntimeError


def main():
    n = int(sys.argv[1])
    lim = int(sys.argv[2])
    backdoor = int(sys.argv[3])
    lim = min(lim, n // 4)
    mapping, count = build_mapping(n, lim)
    dimacs = weak_schur_dimacs(n, mapping, count, lim, backdoor)
    print(dimacs)


if __name__ == '__main__':
    main()
    '''
    n = 643
    lim = 50
    cmd = ["./solvers/lingeling/plingeling", '-n']
    mapping, count = build_mapping(n, lim)
    for backdoor in tqdm.trange(1, 1617):
        dimacs = weak_schur_dimacs(n, mapping, count, lim, backdoor)
        dimacs = dimacs.encode('utf-8')
        result = subprocess.run(cmd, stdout=subprocess.PIPE, input=dimacs)
        if is_solution(result.stdout.decode('utf-8')):
            print(backdoor)
    '''
