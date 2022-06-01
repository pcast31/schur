import sys


def load_partition(filename):
    with open(filename) as file:
        lines = file.readlines()
    partition = []
    for i, line in enumerate(lines, 1):
        for x in map(int, line.split()):
            delta = x - len(partition)
            if delta > 0:
                partition.extend([0] * delta)
            partition[x - 1] = i
    return partition


def parse_filename(filename):
    try:
        filename = filename.split('/')[3]
    except IndexError:
        filename = filename.split('\\')[3]
    filename = filename[2:-5]
    clique_sizes, carac = filename.split(';')
    clique_sizes = clique_sizes.split(',')
    n_col = len(clique_sizes)
    temp_col = clique_sizes.index('t') + 1
    if '-' in carac:
        carac = carac.split('-')
        if len(carac) == 2:
            width, head = map(int, carac)
            extra = 0
        else:
            width, head, extra = map(int, carac)
    else:
        width = int(carac)
        head = 0
        extra = 0
    return n_col, temp_col, width, head, extra


def construct(template, partition, n_col, temp_col, width, head, extra):
    compound = template[:head]
    if extra == 0:
        template = template[head:]
    else:
        ending = template[-extra:]
        template = template[head:-extra]
    for col in partition:
        if col == 1:
            col = temp_col
        else:
            col += n_col - 1
        pattern = [c if c != temp_col else col for c in template]
        compound.extend(pattern)
    if extra == 0:
        for i, c in enumerate(template):
            if c == temp_col:
                break
        compound.extend(template[:i])
    else:
        compound.extend(ending)
    return compound


def get_clique_sizes(filename):
    try:
        filename = filename.split('/')[3]
    except IndexError:
        filename = filename.split('\\')[3]
    filename = filename[2:-5]
    cliques, _ = filename.split(';')
    cliques = cliques.split(',')
    return cliques


def save_partition(cliques, coloring):
    partition = [[] for _ in cliques]
    for x, c in enumerate(coloring, 1):
        partition[c - 1].append(x)
    filename = f"../results/partitions/U({','.join(cliques)};{len(coloring)}).txt"
    with open(filename, 'w') as file:
        for col in partition:
            content = " ".join(map(str, col)) + '\n'
            file.write(content)


def main():
    template_file = sys.argv[1]
    partition_file = sys.argv[2]
    template = load_partition(template_file)
    partition = load_partition(partition_file)
    n_col, temp_col, width, head, extra = parse_filename(template_file)
    compound = construct(template, partition, n_col, temp_col, width, head, extra)
    template_cliques = get_clique_sizes(template_file)
    partition_cliques = get_clique_sizes(partition_file)
    cliques = template_cliques.copy()
    cliques[temp_col - 1] = partition_cliques[0]
    cliques.extend(partition_cliques[1:])
    save_partition(cliques, compound)


if __name__ == '__main__':
    main()
