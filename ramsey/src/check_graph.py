import sys
import numpy as np


def is_coloring(graph, graph_size, n_colors):
    for i in range(graph_size):
        if graph[i, i] != 0:
            print(f"There is an edge between vertex {i} and itself.")
            return False
        for j in range(i + 1, graph_size):
            if graph[i, j] != graph[j, i]:
                print(f"graph[i, j] = {graph[i, j]} but graph[j, i] = {graph[j, i]}.")
                return False
            if graph[i, j] > n_colors:
                print(f"Edge ({i},{j}) has color {graph[i, j]} but there are {n_colors} colors.")
                return False
    return True


def max_clique(graph):
    size = graph.shape[0]
    neighbors = []
    for i in range(size):
        neighbors.append({j for j in range(i + 1, size) if graph[i, j]})
    stack = [([], set(range(size)))]
    largest = []
    while stack:
        clique, neighs = stack.pop()
        if not neighs:
            if len(clique) > len(largest):
                largest = clique
            continue
        for u in neighs:
            next_clique = clique + [u]
            next_neighs = neighs.intersection(neighbors[u])
            stack.append((next_clique, next_neighs))
    return largest


def check_graph(graph, clique_sizes, graph_size):
    if graph.shape != (graph_size, graph_size):
        print(f"Expected graph of size {graph_size} but graph has size {graph.shape[0]}")
        return False
    if not is_coloring(graph, graph_size, len(clique_sizes)):
        return False
    clique_numbers = []
    for c, size in enumerate(clique_sizes, 1):
        subgraph = graph == c
        clique = max_clique(subgraph)
        if len(clique) >= size:
            print(f"The graph contains a clique of size {len(clique)} in color {c}: {clique}.")
            return False
        clique_numbers.append(len(clique))
    print(f"The coloring with {len(clique_sizes)} colors is valid. The graph has size {graph_size}. The clique numbers are {clique_numbers}.")
    return True


def main():
    filename = sys.argv[1]
    graph = np.load(filename)
    try:
        filename = filename.split('/')[3]
    except IndexError:
        filename = filename.split('\\')[3]
    description = filename[2:-5]
    clique_sizes, graph_size = description.split(';')
    graph_size = int(graph_size)
    clique_sizes = list(map(int, clique_sizes.split(',')))
    check_graph(graph, clique_sizes, graph_size)


if __name__ == '__main__':
    main()
