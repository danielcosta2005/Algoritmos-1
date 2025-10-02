
def prob1(g, source):
    dist = g.dijkstra(source)
    print("Parte 1:", dist[g.num_vertices()])  # até o parque (N)

def prob2(g, praca, parque):
    dist1 = g.dijkstra(praca)
    distN = g.dijkstra(parque)
    D = dist1[parque]

    result = []
    for i, (u, v, w) in enumerate(g.get_edges(), start=1):
        if dist1[u] + w + distN[v] == D or dist1[v] + w + distN[u] == D:
            result.append(i)

    if result:
        print("Parte 2:", " ".join(map(str, result)))
    else:
        print("Parte 2: -1")

