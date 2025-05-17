import os
import random
from collections import defaultdict

SOURCE_DIR = "inputs"
RESULT_DIR = "outputs"

class GraphProcessor:
    def __init__(self):
        os.makedirs(RESULT_DIR, exist_ok=True)

    def reset_output_folder(self):
        for f in os.listdir(RESULT_DIR):
            if f.endswith(".txt"):
                os.remove(os.path.join(RESULT_DIR, f))

    def load_graph_data(self, filepath):
        with open(filepath, "r") as f:
            content = f.readlines()

        i = 0
        while content[i].startswith("#"):
            i += 1

        v_count, e_count, g_type = content[i].strip().split()
        v_count, e_count = int(v_count), int(e_count)
        edge_list = content[i+1:-1]
        src_node = content[-1].strip()
        edges = [tuple(line.strip().split()) for line in edge_list]

        return v_count, e_count, g_type, [(u, v, int(w)) for u, v, w in edges], src_node

    def run_dijkstra(self, nodes, edges, source, is_directed):
        distance = {v: float("inf") for v in nodes}
        prev_node = {v: None for v in nodes}
        distance[source] = 0
        visited = set()

        while len(visited) < len(nodes):
            current = min((v for v in nodes if v not in visited), key=lambda x: distance[x], default=None)
            if current is None or distance[current] == float("inf"):
                break
            visited.add(current)

            for x, y, w in edges:
                if is_directed:
                    if x == current and y not in visited and distance[y] > distance[x] + w:
                        distance[y] = distance[x] + w
                        prev_node[y] = x
                else:
                    for a, b in [(x, y), (y, x)]:
                        if a == current and b not in visited and distance[b] > distance[a] + w:
                            distance[b] = distance[a] + w
                            prev_node[b] = a
        return distance, prev_node

    def run_kruskal(self, edges):
        parent = {}
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            parent[px] = py
            return True

        nodes = {u for e in edges for u in (e[0], e[1])}
        for node in nodes:
            parent[node] = node

        total_cost, mst_edges = 0, []
        for u, v, w in sorted(edges, key=lambda x: x[2]):
            if union(u, v):
                mst_edges.append((u, v, w))
                total_cost += w
        return mst_edges, total_cost

    def dfs_with_cycles_and_topo(self, edges, nodes):
        graph = defaultdict(list)
        for u, v, _ in edges:
            graph[u].append(v)

        visited = {}
        cycle_list = []
        topo_sorted = []

        def dfs(v, path):
            visited[v] = "gray"
            path.append(v)
            for neighbor in graph[v]:
                if visited.get(neighbor) == "gray":
                    start = path.index(neighbor)
                    cycle_list.append(path[start:] + [neighbor])
                elif visited.get(neighbor) is None:
                    dfs(neighbor, path)
            visited[v] = "black"
            path.pop()
            topo_sorted.append(v)

        for v in nodes:
            if visited.get(v) is None:
                dfs(v, [])

        return cycle_list, topo_sorted[::-1]

    def pick_graph_files(self, mode):
        files = sorted(os.listdir(SOURCE_DIR))
        random.shuffle(files)
        selected = []

        for f in files:
            path = os.path.join(SOURCE_DIR, f)
            with open(path) as file:
                line = file.readline()
                while line.startswith("#"):
                    line = file.readline()
                try:
                    v, e, t = line.strip().split()
                    v, e = int(v), int(e)
                    is_d = t == "D"

                    if mode == "1" and v >= 17 and e >= 35:
                        selected.append(f)
                    elif mode == "2" and v >= 17 and e >= 35:
                        selected.append(f)
                    elif mode == "3" and is_d and v >= 17 and e >= 35:
                        selected.append(f)

                    if len(selected) == 5:
                        break
                except ValueError:
                    print(f"⚠️ Skipping invalid file format: {f}")
                    continue

        return selected

    def execute(self):
        self.reset_output_folder()

        print("🧠 Choose Operation:")
        print("1. Dijkstra Algorithm")
        print("2. Kruskal’s MST")
        print("3. DFS Topological Sort and Cycle Detection")
        mode = input("Select (1/2/3): ").strip()

        input_files = self.pick_graph_files(mode)
        if not input_files:
            print("❌ No suitable input files found.")
            return

        for filename in input_files:
            print(f"\n🔍 Processing {filename}...")
            v, e, typ, edges, source = self.load_graph_data(os.path.join(SOURCE_DIR, filename))
            nodes = sorted(set(x for edge in edges for x in (edge[0], edge[1])))
            directed = typ == "D"
            output_path = os.path.join(RESULT_DIR, filename.replace(".txt", "_output.txt"))

            with open(output_path, "w") as out:
                out.write(f"# Graph Type: {'Directed' if directed else 'Undirected'}\n")
                out.write(f"# Vertices: {v}, Edges: {e}\n\n")

                if mode == "1":
                    dist, prev = self.run_dijkstra(nodes, edges, source, directed)
                    for node in nodes:
                        if dist[node] < float("inf"):
                            path = []
                            current = node
                            while current:
                                path.append(current)
                                current = prev[current]
                            out.write(f"Path to {node}: {' -> '.join(reversed(path))} | Cost: {dist[node]}\n")
                        else:
                            out.write(f"No path to {node}\n")

                elif mode == "2":
                    undirected_edges = {(min(u, v), max(u, v), w) for u, v, w in edges}
                    mst, cost = self.run_kruskal(list(undirected_edges))
                    out.write("MST Edges:\n")
                    for u, v, w in mst:
                        out.write(f"{u} - {v} : {w}\n")
                    out.write(f"Total MST cost: {cost}\n")

                elif mode == "3":
                    if not directed:
                        print(f"⚠️ Skipping {filename}: Topological sort requires directed graphs.")
                        continue
                    cycles, topo = self.dfs_with_cycles_and_topo(edges, nodes)
                    if cycles:
                        out.write("Cycles found:\n")
                        for c in cycles:
                            out.write(f"{' -> '.join(c)} | Length: {len(c)}\n")
                    else:
                        out.write("Topological Order:\n")
                        out.write(" -> ".join(topo) + "\n")

if __name__ == "__main__":
    GraphProcessor().execute()
