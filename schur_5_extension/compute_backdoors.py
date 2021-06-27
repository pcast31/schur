import subprocess
import tqdm


N_BACKDOORS = 1616
SAT_SOLVER = ["./solvers/lingeling/lingeling", '-n']


def generate_dimacs():
    for i in tqdm.trange(1, N_BACKDOORS + 1):
        cmd = ["./apply.sh", "Schur_160_5_SBP.cnf", "backdoors.cubes", str(i)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        dimacs = result.stdout.decode('utf-8')
        filename = f"dimacs_files/Schur-5-{i}.cnf"
        with open(filename, mode='w') as file:
            file.write(dimacs)


def get_fixed_dimacs(i):
    filename = f'dimacs_files/Schur-5-{i}.cnf'
    with open(filename) as dimacs:
        n_clauses = int(dimacs.readline().split()[-1]) + 1
        header = f"p cnf 800 {n_clauses}\n"
        clauses = dimacs.readlines()
    fixed_dimacs = header + ''.join(clauses)
    return fixed_dimacs


def is_solution(answer):
    for line in answer.splitlines():
        if line[0] != 's':
            continue
        return line[2] == 'S'
    raise RuntimeError


def compute_backdoor(fixed_dimacs):
    backdoor = []
    for a in range(160):
        possibilities = []
        for c in range(1, 6):
            dimacs = fixed_dimacs + f"{5 * a + c} 0\n"
            dimacs = dimacs.encode('utf-8')
            result = subprocess.run(SAT_SOLVER, stdout=subprocess.PIPE,
                                    input=dimacs)
            if is_solution(result.stdout.decode('utf-8')):
                possibilities.append(c)
        backdoor.append(possibilities)
    return backdoor


def sort_colours(backdoor):
    colours = [[] for _ in range(5)]
    for a, possibilities in enumerate(backdoor):
        for c in possibilities:
            colours[c - 1].append(a)
    colours.sort(key=min)
    backdoor = [[] for _ in range(160)]
    for c, colour in enumerate(colours):
        for a in colour:
            backdoor[a].append(c + 1)
    backdoor = [' '.join(map(str, possibilities)) for possibilities in backdoor]
    return backdoor


def compute_backdoors():
    for i in tqdm.trange(1, N_BACKDOORS + 1):
        fixed_dimacs = get_fixed_dimacs(i)
        backdoor = compute_backdoor(fixed_dimacs)
        backdoor = sort_colours(backdoor)
        content = '\n'.join(backdoor)
        filename = f"backdoors/backdoor-{i}"
        with open(filename, mode='w') as file:
            file.write(content)


def main():
    print(f"\n\nThere are {N_BACKDOORS} backdoors.")
    print("\n\ngenerating dimacs files\n")
    generate_dimacs()
    print("\ndone")
    print("\n\ncomputing backdoors\n")
    compute_backdoors()
    print("\ndone\n\n")


if __name__ == '__main__':
    main()
