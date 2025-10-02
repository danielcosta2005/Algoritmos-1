import heapq

class Graph:
    def __init__(self, n, m):
        self.n = n  # número de vértices
        self.m = m  # número de arestas
        self.adj = [[] for _ in range(n + 1)]  # adj[1] contém os vizinhos do vértice 1, etc...
        self.edges = []  # lista de arestas (u,v,w) na ordem da entrada

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))  # não direcionado
        self.edges.append((u, v, w)) # guarda também na lista de arestas

    def neighbors(self, u):
        return self.adj[u]

    def num_vertices(self):
        return self.n

    def num_edges(self):
        return self.m
    
    def get_edges(self):
        return self.edges
    
    def dijkstra(self, source):
        n = self.num_vertices()
        dist = [float("inf")] * (n + 1) # cria lista de tamanho n+1 com valores infinitos  
        dist[source] = 0
        
        minheap = [(0, source)]  # (distância acumulada, vértice)
        
        while minheap:
            d, u = heapq.heappop(minheap)
            if d > dist[u]:
                continue # lida com distancias obsoletas
            for v, w in self.neighbors(u):
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(minheap, (dist[v], v))
        
        return dist
