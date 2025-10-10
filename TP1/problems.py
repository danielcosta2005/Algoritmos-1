from graph import Graph

def prob1(g, source):
    dist = g.dijkstra(source)
    print("Parte 1:", dist[g.num_vertices()])  # até o parque (N)

def prob2(g, praca, parque):
    dist1 = g.dijkstra(praca)
    distN = g.dijkstra(parque)
    D = dist1[parque]

    n = g.num_vertices()
    subgrafo = Graph(n, 0)  # cria um novo grafo vazio (subgrafo)
    result = []

    for i, (u, v, w) in enumerate(g.get_edges(), start=1):
        if dist1[u] + w + distN[v] == D or dist1[v] + w + distN[u] == D:
            result.append(i)
            subgrafo.add_edge(u, v, i)  # usa o índice como "peso", pra rastrear a rua

    return result, subgrafo


def prob3(subgrafo, praca):
    criticas = subgrafo.dfs_bridges(praca) # descobre as arestas que deixam o subgrafo desconexo (pontes)

    if criticas:
        print("Parte 3:", " ".join(map(str, sorted(criticas))))
    else:
        print("Parte 3: -1")

