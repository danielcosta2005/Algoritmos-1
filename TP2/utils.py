import sys

def load_data():
    # Lê todo o conteúdo da entrada padrão
    entrada = sys.stdin.read().strip().split()

    # Índice que usaremos para percorrer os valores da entrada
    pos = 0

    # Parte 1
    N = int(entrada[pos])
    pos += 1

    blocos = []
    for i in range(N):
        valor = int(entrada[pos])
        blocos.append(valor)
        pos += 1

    # Parte 2
    Z = int(entrada[pos])
    pos += 1

    arvores = []
    for i in range(Z):
        x = int(entrada[pos])
        y = int(entrada[pos + 1])
        arvores.append((x, y))
        pos += 2

    return N, blocos, Z, arvores
