from utils import caso_base, dividir, escolher_melhor_lado, merge_faixa

def parte1(N, blocos):
    # Alturas possíveis crescendo da esquerda para a direita
    alto_esq = [0] * N
    for i in range(N):
        if i == 0:
            alto_esq[i] = min(blocos[i], 1)
        else:
            # posso crescer no máximo 1 em relação à anterior
            alto_esq[i] = min(blocos[i], alto_esq[i - 1] + 1)

    # Alturas possíveis crescendo da direita para a esquerda 
    alto_dir = [0] * N
    for i in range(N - 1, -1, -1):
        if i == N - 1:
            alto_dir[i] = min(blocos[i], 1)
        else:
            alto_dir[i] = min(blocos[i], alto_dir[i + 1] + 1)

    # Combina os dois lados e pega o máximo 
    melhor_altura = 0
    for i in range(N):
        altura_i = min(alto_esq[i], alto_dir[i])
        if altura_i > melhor_altura:
            melhor_altura = altura_i

    return melhor_altura

def divisao_conquista(px, py):
    """
    Função principal de divisão e conquista.
    px: pontos ordenados por x
    py: pontos ordenados por y
    """
    n = len(px)

    # 1. caso base
    if n <= 5:
        return caso_base(px)

    # 2. divide em esquerda/direita
    px_esq, px_dir, py_esq, py_dir, midx = dividir(px, py)

    # 3. resolve recursivamente os dois lados
    per_esq, trip_esq = divisao_conquista(px_esq, py_esq)
    per_dir, trip_dir = divisao_conquista(px_dir, py_dir)

    # 4. escolhe o melhor entre esquerda e direita
    melhor_per, melhor_tripla = escolher_melhor_lado(per_esq, trip_esq,
                                                     per_dir, trip_dir)

    # 5. tenta melhorar olhando triplas que atravessam a linha de divisão
    melhor_per, melhor_tripla = merge_faixa(py, midx, melhor_per, melhor_tripla)

    return melhor_per, melhor_tripla


def parte2(arvores):
    px = sorted(arvores, key=lambda p: p[0])  # ordena por coordenada x
    py = sorted(arvores, key=lambda p: p[1])  # ordena por coordenada y

    melhor_per, melhor_tripla = divisao_conquista(px, py)
    a1, a2, a3 = melhor_tripla
    return melhor_per, a1, a2, a3
