from utils import lex_less_global, lex_less_local

def preprocess_right_half(left_size, right_size, conflict_masks):
    """
    Processa todos os subconjuntos da metade direita (tamanho right_size),
    determinando se são independentes e qual o seu tamanho.

    Retorna:
        sizeR[mask]       -- tamanho do subset se independente, ou -inf se não
        base_maskR[mask]  -- o próprio mask se independente, ou 0 se não
    """
    R = right_size

    if R == 0:
        # Sem metade direita: só o conjunto vazio
        return [0], [0]

    num_masks = 1 << R
    independentR = [False] * num_masks
    sizeR = [-10**9] * num_masks
    base_maskR = [0] * num_masks

    independentR[0] = True
    sizeR[0] = 0
    base_maskR[0] = 0

    for mask in range(1, num_masks):
        lsb = mask & -mask
        v_local = lsb.bit_length() - 1
        prev = mask ^ lsb

        if not independentR[prev]:
            independentR[mask] = False
            sizeR[mask] = -10**9
            continue

        v_global = left_size + v_local
        global_prev_mask = prev << left_size  # prev só vive na direita

        # Se v_global briga com alguém de prev (na direita), não é independente
        if conflict_masks[v_global] & global_prev_mask:
            independentR[mask] = False
            sizeR[mask] = -10**9
        else:
            independentR[mask] = True
            sizeR[mask] = sizeR[prev] + 1
            base_maskR[mask] = mask

    return sizeR, base_maskR



def build_right_dp(right_size, sizeR, base_maskR):
    """
    A partir dos subsets independentes da direita (sizeR/base_maskR),
    constrói o DP de superconjunto:

        best_sizeR[mask] = maior tamanho de subset independente contido em mask
        best_maskR[mask] = o próprio subset (em índices locais da direita)
    """
    R = right_size
    num_masks = 1 << R

    best_sizeR = sizeR[:]       # começa com: -inf ou tamanho do subset inteiro se independente
    best_maskR = base_maskR[:]  # 0 se não-independente, mask se independente

    for i in range(R):
        bit = 1 << i
        for mask in range(num_masks):
            if mask & bit:
                other = mask ^ bit
                if best_sizeR[other] > best_sizeR[mask]:
                    best_sizeR[mask] = best_sizeR[other]
                    best_maskR[mask] = best_maskR[other]
                elif best_sizeR[other] == best_sizeR[mask]:
                    # Empate de tamanho: escolhe lexicograficamente menor
                    if lex_less_local(best_maskR[other], best_maskR[mask], R):
                        best_maskR[mask] = best_maskR[other]

    return best_sizeR, best_maskR


def combine_halves(N, left_size, right_size, conflict_masks, best_sizeR, best_maskR):
    """
    Enumera todos os subconjuntos da metade esquerda, verifica independência e,
    para cada um, combina com a melhor escolha possível da metade direita
    (respeitando conflitos).

    Retorna:
        best_global_size, best_global_mask
    """
    L = left_size
    R = right_size

    full_right_mask = (1 << R) - 1
    num_left_masks = 1 << L

    independentL = [False] * num_left_masks
    sizeL = [-10**9] * num_left_masks
    union_conflicts_B_local = [0] * num_left_masks  # conflitos com a direita, em índices locais

    # Conjunto vazio da esquerda é sempre independente
    independentL[0] = True
    sizeL[0] = 0
    union_conflicts_B_local[0] = 0

    best_global_size = -1
    best_global_mask = 0

    for mask in range(num_left_masks):
        if mask != 0:
            # Pegamos o último bit incluído para construir mask a partir de prev
            lsb = mask & -mask
            v_local = lsb.bit_length() - 1
            prev = mask ^ lsb

            if not independentL[prev]:
                independentL[mask] = False
                sizeL[mask] = -10**9
            else:
                v_global = v_local  # na esquerda, índices locais = globais
                global_prev_mask = prev  # só mexe em bits 0..L-1

                # Checa conflitos internos na esquerda
                if conflict_masks[v_global] & global_prev_mask:
                    independentL[mask] = False
                    sizeL[mask] = -10**9
                else:
                    independentL[mask] = True
                    sizeL[mask] = sizeL[prev] + 1

                    # Atualiza conflitos com a direita:
                    # conflict_masks[v_global] tem bits 0..N-1
                    # shift à direita para alinhar [L..N-1] em 0..R-1
                    conflicts_with_right_local = conflict_masks[v_global] >> L
                    union_conflicts_B_local[mask] = (
                        union_conflicts_B_local[prev] | conflicts_with_right_local
                    )

        if not independentL[mask]:
            continue

        # Conjunto de vértices proibidos na direita, em índices 0..R-1
        forbidden_B_local = union_conflicts_B_local[mask] & full_right_mask
        allowed_B_mask = full_right_mask & (~forbidden_B_local)

        size_left = sizeL[mask]
        size_right = best_sizeR[allowed_B_mask] if R > 0 else 0

        total_size = size_left + size_right
        if total_size < 0:
            continue

        # Reconstrói a escolha na direita
        right_choice_local = best_maskR[allowed_B_mask] if R > 0 else 0
        # Monta máscara global (esquerda em [0..L-1], direita em [L..N-1])
        global_mask = mask | (right_choice_local << L)

        if total_size > best_global_size:
            best_global_size = total_size
            best_global_mask = global_mask
        elif total_size == best_global_size and best_global_size >= 0:
            if lex_less_global(global_mask, best_global_mask, N):
                best_global_mask = global_mask

    # Garantia de pelo menos conjunto vazio
    if best_global_size < 0:
        best_global_size = 0
        best_global_mask = 0

    return best_global_size, best_global_mask


def max_independent_set(N, conflict_masks):
    """
    Resolve o problema do conjunto independente máximo (Maximum Independent Set)
    usando meet-in-the-middle com DP em bitmasks.

    Retorna:
        best_size (int): tamanho máximo
        best_mask (int): bitmask dos duendes escolhidos (0..N-1)
    """
    left_size = N // 2
    right_size = N - left_size

    # 1) Pré-processa a metade direita (subconjuntos independentes)
    sizeR, base_maskR = preprocess_right_half(left_size, right_size, conflict_masks)

    # 2) Constrói o DP de superconjuntos na direita
    best_sizeR, best_maskR = build_right_dp(right_size, sizeR, base_maskR)

    # 3) Enumera a esquerda e combina com a direita
    best_global_size, best_global_mask = combine_halves(
        N, left_size, right_size, conflict_masks, best_sizeR, best_maskR
    )

    return best_global_size, best_global_mask

