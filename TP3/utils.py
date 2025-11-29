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

def build_conflict_masks(N, conflitos):
    """
    Constrói, para cada duende i, uma máscara de bits indicando
    com quais duendes ele briga.

    conflict_masks[i] é um inteiro onde o bit j está 1 se (i, j) é um conflito.
    """
    conflict_masks = [0] * N

    for a, b in conflitos:
        if a == b:
            # Se por acaso vier algo assim, ignoramos (não faz sentido brigar consigo mesmo)
            continue
        conflict_masks[a] |= (1 << b) # Coloca um "1" na posição b
        conflict_masks[b] |= (1 << a)

    return conflict_masks

def lex_less_local(mask1, mask2, size):
    """
    Compara dois subconjuntos de {0, ..., size-1} representados por bitmasks.

    Retorna True se mask1 é lexicograficamente menor que mask2.
    """
    if mask1 == mask2:
        return False

    for i in range(size):
        b1 = bool(mask1 & (1 << i))
        b2 = bool(mask2 & (1 << i))

        if b1 != b2:          # achou o primeiro bit diferente
            if b1 == 1 and b2 == 0:
                return True   # mask1 é lexicograficamente menor
            else:
                return False  # mask1 é maior
            
    return False  # iguais (mas já teríamos retornado antes)
    

def lex_less_global(mask1, mask2, N):
    """
    Compara dois subconjuntos de {0, ..., N-1} representados por bitmasks.

    Retorna True se mask1 é lexicograficamente menor que mask2.
    """
    if mask1 == mask2:
        return False

    for i in range(N):
        b1 = bool(mask1 & (1 << i))
        b2 = bool(mask2 & (1 << i))

        if b1 != b2:          
            if b1 == 1 and b2 == 0:
                return True   
            else:
                return False  

    return False

def extract_idxs(N, best_mask):
    # Extrai índices em ordem crescente
    escolhidos = []
    for i in range(N):
        if best_mask & (1 << i):
            escolhidos.append(i)
    
    return escolhidos
