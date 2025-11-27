import sys
import math

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
    for i in range(1, Z+1):
        x = int(entrada[pos])
        y = int(entrada[pos + 1])
        arvores.append((x, y, i))
        pos += 2

    return N, blocos,arvores

def distancia(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def perimetro(p1, p2, p3):
    return (distancia(p1, p2)
            + distancia(p2, p3)
            + distancia(p1, p3))

def melhor_tripla_atual(per_atual, tripla_atual, per_novo, tripla_nova):
    if per_novo < per_atual:
        return per_novo, tripla_nova
    elif abs(per_novo - per_atual) < 1e-9:
        if tripla_nova < tripla_atual:
            return per_novo, tripla_nova
    return per_atual, tripla_atual

def caso_base(pontos):
    """
    Resolve por força bruta quando o número de pontos é pequeno.
    'pontos' vem ordenado por x, mas isso não importa aqui.
    """
    n = len(pontos)
    melhor_per = float('inf')
    melhor_tripla = None

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                p1, p2, p3 = pontos[i], pontos[j], pontos[k]
                per = perimetro(p1, p2, p3)
                idxs = sorted([p1[2], p2[2], p3[2]])
                melhor_per, melhor_tripla = melhor_tripla_atual(
                    melhor_per, melhor_tripla,
                    per, tuple(idxs)
                )

    return melhor_per, melhor_tripla


def dividir(px, py):
    """
    Divide o problema em duas metades:
      - px_esq, px_dir (ordenadas por x)
      - py_esq, py_dir (ordenadas por y)
    Retorna também o x da linha de corte (midx).
    """
    n = len(px)
    mid = n // 2
    midx = px[mid][0]

    px_esq = px[:mid]
    px_dir = px[mid:]

    # separar py respeitando as mesmas metades
    esq_set = {(p[0], p[1], p[2]) for p in px_esq}
    py_esq = []
    py_dir = []
    for p in py:
        if (p[0], p[1], p[2]) in esq_set:
            py_esq.append(p)
        else:
            py_dir.append(p)

    return px_esq, px_dir, py_esq, py_dir, midx


def escolher_melhor_lado(per_esq, trip_esq, per_dir, trip_dir):
    """
    Decide qual dos dois lados (esquerda ou direita) tem o melhor triângulo.
    Em caso de empate de perímetro, aplica o critério lexicográfico.
    """
    if per_esq < per_dir:
        return per_esq, trip_esq
    if per_dir < per_esq:
        return per_dir, trip_dir

    # perímetros iguais (considerando tolerância)
    if abs(per_esq - per_dir) < 1e-9:
        if trip_esq < trip_dir:
            return per_esq, trip_esq
        else:
            return per_dir, trip_dir

    # fallback (não deve cair aqui)
    return per_esq, trip_esq


def merge_faixa(py, midx, melhor_per, melhor_tripla):
    """
    Etapa de combinação:
      - pega apenas os pontos próximos da linha de divisão (faixa)
      - testa triplas nessa faixa para tentar melhorar o resultado
    """
    faixa = []
    limite = melhor_per / 2.0

    # pega só os pontos que estão perto da linha de corte
    for p in py:
        if abs(p[0] - midx) <= limite:
            faixa.append(p)

    max_vizinhos = 20
    m = len(faixa)

    for i in range(m):
        for j in range(i + 1, min(i + 1 + max_vizinhos, m)):
            for k in range(j + 1, min(j + 1 + max_vizinhos, m)):
                p1, p2, p3 = faixa[i], faixa[j], faixa[k]
                per = perimetro(p1, p2, p3)
                if per <= melhor_per + 1e-9:
                    idxs = sorted([p1[2], p2[2], p3[2]])
                    melhor_per, melhor_tripla = melhor_tripla_atual(
                        melhor_per, melhor_tripla,
                        per, tuple(idxs)
                    )

    return melhor_per, melhor_tripla
