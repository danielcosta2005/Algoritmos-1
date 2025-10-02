class Graph:
    def __init__(self, n, m):
        self.n = n  # número de vértices
        self.m = m  # número de arestas
        self.adj = [[] for _ in range(n + 1)]  # adj[1] contém os vizinhos do vértice 1, etc...

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))  # não direcionado

    def neighbors(self, u):
        return self.adj[u]

    def num_vertices(self):
        return self.n

    def num_edges(self):
        return self.m
