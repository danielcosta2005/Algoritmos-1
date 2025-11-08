from graph import Graph
import sys

def load_data():
    data = sys.stdin.read().strip().split()
    
    n = int(data[0])  # número de regiões
    m = int(data[1])  # número de ruas
    
    g = Graph(n, m)
    
    # percorre os M blocos (Ai, Bi, Ci)
    idx = 2
    for _ in range(m):
        u = int(data[idx])
        v = int(data[idx + 1])
        w = int(data[idx + 2])
        g.add_edge(u, v, w)
        idx += 3
    
    return g
