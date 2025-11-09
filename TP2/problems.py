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


