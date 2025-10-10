
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

def prob3(g, praca, parque):
    # 1. Calcula a distância mínima original
    dist_original = g.dijkstra(praca)
    menor_distancia = dist_original[parque]

    ruas_criticas = []

    # 2. Testa cada rua (aresta)
    for i, (u, v, w) in enumerate(g.get_edges(), start=1):

        # Remove temporariamente a aresta (u, v) 
        nova_lista_u = []
        for (vizinho, peso) in g.adj[u]:
            if not (vizinho == v and peso == w):
                nova_lista_u.append((vizinho, peso))
        g.adj[u] = nova_lista_u

        nova_lista_v = []
        for (vizinho, peso) in g.adj[v]:
            if not (vizinho == u and peso == w):
                nova_lista_v.append((vizinho, peso))
        g.adj[v] = nova_lista_v

        # Recalcula a nova distância da praça ao parque 
        nova_distancia = g.dijkstra(praca)[parque]

        # Recoloca a aresta removida 
        g.adj[u].append((v, w))
        g.adj[v].append((u, w))

        # Verifica se essa rua é crítica 
        if nova_distancia > menor_distancia or nova_distancia == float("inf"):
            ruas_criticas.append(i)

    # 3. Exibe o resultado
    if ruas_criticas:
        print("Parte 3:", " ".join(map(str, ruas_criticas)))
    else:
        print("Parte 3: -1")

