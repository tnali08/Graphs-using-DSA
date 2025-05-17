import os
import random

DATA_DIR = "inputs"
VERTICES_UDG = 18
VERTICES_DG = 17
TOTAL_EDGES = 35

def create_node_labels(count):
    return [chr(65 + i) for i in range(count)]

def build_undirected_graph(n_nodes, n_edges, include_cycle=True):
    nodes = create_node_labels(n_nodes)
    edge_set = set()

    if not include_cycle:
        for i in range(n_nodes - 1):
            edge_set.add((nodes[i], nodes[i + 1], random.randint(1, 20)))

    while len(edge_set) < n_edges:
        u, v = random.sample(nodes, 2)
        ordered = tuple(sorted((u, v)))
        if ordered not in {(a, b) for a, b, _ in edge_set} and u != v:
            edge_set.add((ordered[0], ordered[1], random.randint(1, 20)))

    return nodes, list(edge_set)

def build_directed_graph(n_nodes, n_edges, include_cycle=True):
    nodes = create_node_labels(n_nodes)
    edge_set = set()

    if not include_cycle:
        while len(edge_set) < n_edges:
            u, v = random.sample(nodes, 2)
            if nodes.index(u) < nodes.index(v):
                edge_set.add((u, v, random.randint(1, 20)))
    else:
        while len(edge_set) < n_edges - 1:
            u, v = random.sample(nodes, 2)
            edge_set.add((u, v, random.randint(1, 20)))
        edge_set.add((nodes[-1], nodes[0], random.randint(1, 20)))

    return nodes, list(edge_set)

def export_graph_file(name, vertices, connections, g_type):
    with open(os.path.join(DATA_DIR, name), "w") as f:
        f.write(f"# Graph Type: {'Directed' if g_type == 'D' else 'Undirected'}\n")
        f.write(f"# Vertices: {len(vertices)}, Edges: {len(connections)}\n")
        f.write(f"{len(vertices)} {len(connections)} {g_type}\n")
        for u, v, w in connections:
            f.write(f"{u} {v} {w}\n")
        f.write(f"{vertices[0]}\n")

def run_generator():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Generate 5 undirected graphs
    for i in range(1, 6):
        cyclic = i % 2 == 1
        nodes, links = build_undirected_graph(VERTICES_UDG, TOTAL_EDGES, cyclic)
        export_graph_file(f"custom_undirected_{i}.txt", nodes, links, "U")

    # Generate 5 directed graphs
    for i in range(1, 6):
        cyclic = i % 2 == 0
        nodes, links = build_directed_graph(VERTICES_DG, TOTAL_EDGES, cyclic)
        export_graph_file(f"custom_directed_{i}.txt", nodes, links, "D")

    print("🎉 Graph generation complete: 10 files saved in 'inputs/'.")

if __name__ == "__main__":
    run_generator()
