import subprocess
import sys
import tqdm


def is_solution(answer):
    for line in answer.splitlines():
        if line[0] != 's':
            continue
        return line[2] == 'S'
    print(answer)
    raise RuntimeError


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


def search_space(k, n, i, c_i, m_4):
    cnf = [f"{k * (i - 1) + c_i}"]
    for j in range(1, m_4):
        cnf.append(f"-{k * (j - 1) + 4}")
    cnf.append(f"{k * (m_4 - 1) + 4}")
    return cnf


def weak_schur_cnf(k, n, i, c_i, m_4):
    cnf = weakly_sum_free(k, n)
    cnf.extend(use_all(k, n))
    cnf.extend(disjoint(k, n))
    cnf.extend(break_symmetries(k))
    cnf.extend(search_space(k, n, i, c_i, m_4))
    return cnf


def weak_schur_dimacs(k, n, i, c_i, m_4):
    cnf = weak_schur_cnf(k, n, i, c_i, m_4)
    text = f"p cnf {k * n} {len(cnf)}\n" + " 0\n".join(cnf) + " 0\n"
    return text


def main():
    k = 4
    n = int(sys.argv[1])
    m_4 = int(sys.argv[2])
    pos = []

    for i in tqdm.tqdm(range(1, n + 1)):
        pos.append([])
        for c_i in range(1, k + 1):
            dimacs = weak_schur_dimacs(k, n, i, c_i, m_4).encode('utf-8')
            cmd = ["../solvers/lingeling/plingeling", '-n']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, input=dimacs)
            if is_solution(result.stdout.decode('utf-8')):
                pos[-1].append(c_i)

    print()
    for p in pos:
        print(*p)


if __name__ == "__main__":
    main()
