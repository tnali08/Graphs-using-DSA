Graph Algorithms Project (Python)
==================================

This project implements three core graph algorithms using pure Python:

1. Dijkstra's Algorithm – for finding the shortest paths from a source node.
2. Kruskal's Algorithm – for computing a Minimum Spanning Tree (MST).
3. DFS with Topological Sort and Cycle Detection – for analyzing directed graphs.

----------------------
Project Structure
----------------------

.
├── inputs/                     → Graph input files (auto-generated)
├── outputs/                    → Algorithm results written here
├── graph_generator_custom.py   → Generates random graphs with/without cycles
├── graph_solver_custom.py      → Runs selected algorithm on input graphs
└── README.txt                  → This file

----------------------
How to Run
----------------------

✓ Requires Python 3.6+
✓ No external libraries needed

Step 1: Generate Graph Input Files
----------------------------------
Run:
    python graph create.py

This creates 10 graphs:
- 5 Undirected (for Kruskal and Dijkstra)
- 5 Directed (some cyclic, some acyclic for DFS/Topo)

Each graph file includes:
- Comment lines for metadata
- Number of vertices, edges, and graph type
- List of edges with weights
- A source node (used by Dijkstra)

Step 2: Run Graph Algorithms
----------------------------
Run:
    python main.py

You will be prompted to choose one of the options:

    1. Dijkstra (SSSP)
    2. Kruskal (MST)
    3. DFS Topological Sort / Cycle Detection

The script will:
- Pick 5 valid input graphs randomly
- Run the selected algorithm
- Save results to the 'outputs/' folder

----------------------
Notes
----------------------
- Uses only Python’s built-in libraries (os, random, collections)
- Algorithms provide:
  • Paths and costs (Dijkstra)
  • MST edges and total cost (Kruskal)
  • Topological order or all cycles (DFS)

----------------------
Sample Input File Format
----------------------

# Graph Type: Undirected
# Vertices: 18, Edges: 35
18 35 U
A B 5
B C 2
...
A

----------------------
Sample Output Format (Kruskal)
----------------------

# Graph Type: Undirected
# Vertices: 18, Edges: 35

MST Edges:
A - B : 3
C - D : 2
...

Total MST cost: 106

----------------------
Author
----------------------
TEJASWI

----------------------
Dependencies
----------------------

None. Uses only:
- os
- random
- collections
