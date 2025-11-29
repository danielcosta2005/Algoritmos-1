from utils import lex_less_global, lex_less_local

def max_independent_set(N, conflict_masks):
    """
    Resolve o problema do conjunto independente máximo (Maximum Independent Set)
    usando meet-in-the-middle com DP em bitmasks.

    Retorna:
        best_size (int): tamanho máximo
        best_mask (int): bitmask dos duendes escolhidos (0..N-1)
    """

    # Divide em duas metades
    left_size = N // 2
    right_size = N - left_size

    # Máscaras globais úteis
    full_right_mask = (1 << right_size) - 1

    # -----------------------------
    # 1) Processar metade direita: todos subconjuntos e ver quais são independentes
    # -----------------------------
    R = right_size
    if R > 0:
        independentR = [False] * (1 << R)
        sizeR = [0] * (1 << R)

        independentR[0] = True
        sizeR[0] = 0

        # Para reconstrução: se um subset é independente, base_maskR[mask] = mask, senão 0
        base_maskR = [0] * (1 << R)

        for mask in range(1, 1 << R):
            lsb = mask & -mask
            v_local = (lsb.bit_length() - 1)  # índice do bit menos significativo
            prev = mask ^ lsb

            if not independentR[prev]:
                independentR[mask] = False
                sizeR[mask] = -10**9
                continue

            v_global = left_size + v_local  # índice real no grafo
            # Conjunto global correspondente ao prev, mas só na direita
            global_prev_mask = prev << left_size

            # Checa se v_global conflita com alguém de prev (apenas direita)
            if conflict_masks[v_global] & global_prev_mask:
                independentR[mask] = False
                sizeR[mask] = -10**9
            else:
                independentR[mask] = True
                sizeR[mask] = sizeR[prev] + 1
                base_maskR[mask] = mask
    else:
        # Sem metade direita
        independentR = [True]
        sizeR = [0]
        base_maskR = [0]

    # -----------------------------
    # 2) DP de superconjunto (SOS DP) na direita
    #    best_sizeR[mask] = melhor tamanho de subconjunto independente contido em mask
    #    best_maskR[mask] = próprio subconjunto (em índices locais da direita)
    # -----------------------------
    best_sizeR = sizeR[:]        # começa com -inf ou o tamanho do próprio subset se independente
    best_maskR = base_maskR[:]   # 0 se não-independente, mask se independente

    for i in range(R):
        bit = 1 << i
        for mask in range(1 << R):
            if mask & bit:
                other = mask ^ bit
                if best_sizeR[other] > best_sizeR[mask]:
                    best_sizeR[mask] = best_sizeR[other]
                    best_maskR[mask] = best_maskR[other]
                elif best_sizeR[other] == best_sizeR[mask]:
                    # Empate: pega a máscara lexicograficamente menor
                    if lex_less_local(best_maskR[other], best_maskR[mask], R):
                        best_maskR[mask] = best_maskR[other]

    # -----------------------------
    # 3) Enumerar subconjuntos da metade esquerda
    # -----------------------------
    L = left_size
    independentL = [False] * (1 << L)
    sizeL = [0] * (1 << L)
    # union_conflicts_B_local[maskL] guarda a união dos conflitos
    # que os vértices de maskL têm com a metade direita (em índices locais 0..R-1)
    union_conflicts_B_local = [0] * (1 << L)

    independentL[0] = True
    sizeL[0] = 0
    union_conflicts_B_local[0] = 0

    best_global_size = -1
    best_global_mask = 0

    for mask in range(1 << L):
        if mask != 0:
            lsb = mask & -mask
            v_local = (lsb.bit_length() - 1)
            prev = mask ^ lsb

            if not independentL[prev]:
                independentL[mask] = False
                sizeL[mask] = -10**9
            else:
                v_global = v_local  # na esquerda, índices globais coincidem
                global_prev_mask = prev  # já está na faixa 0..L-1

                # checa conflitos dentro da esquerda
                if conflict_masks[v_global] & global_prev_mask:
                    independentL[mask] = False
                    sizeL[mask] = -10**9
                else:
                    independentL[mask] = True
                    sizeL[mask] = sizeL[prev] + 1

                    # Atualiza conflitos com a metade direita
                    # Pega conflitos de v_global apenas com vértices da direita:
                    # shift à direita descarta bits 0..L-1, deixando só [L..N-1] alinhados em 0..R-1
                    conflicts_with_right_local = conflict_masks[v_global] >> L
                    union_conflicts_B_local[mask] = union_conflicts_B_local[prev] | conflicts_with_right_local

        if not independentL[mask]:
            continue

        # Para esse subset da esquerda, calcula quais vértices da direita estão proibidos
        forbidden_B_local = union_conflicts_B_local[mask] & full_right_mask
        allowed_B_mask = full_right_mask & (~forbidden_B_local)

        size_left = sizeL[mask]
        size_right = best_sizeR[allowed_B_mask] if R > 0 else 0

        total_size = size_left + size_right

        if total_size < 0:
            continue

        # Monta máscara global completa (esquerda + direita)
        right_choice_local = best_maskR[allowed_B_mask] if R > 0 else 0
        global_mask = mask | (right_choice_local << L)

        if total_size > best_global_size:
            best_global_size = total_size
            best_global_mask = global_mask
        elif total_size == best_global_size and best_global_size >= 0:
            # Empate: escolher solução lexicograficamente mínima
            if lex_less_global(global_mask, best_global_mask, N):
                best_global_mask = global_mask

    # Caso extremo: se nada deu certo, pelo menos conjunto vazio é válido
    if best_global_size < 0:
        best_global_size = 0
        best_global_mask = 0

    return best_global_size, best_global_mask
