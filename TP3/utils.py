import sys

def load_data():
    # Lê todo o conteúdo da entrada padrão como strings
    entrada = sys.stdin.read().strip().split()

    pos = 0

    # Lê N e M
    N = int(entrada[pos])
    pos += 1

    M = int(entrada[pos])
    pos += 1

    # Lê os pares de conflitos
    conflicts = []
    for _ in range(M):
        a = int(entrada[pos])
        b = int(entrada[pos + 1])
        conflicts.append((a, b))
        pos += 2

    return N, conflicts
