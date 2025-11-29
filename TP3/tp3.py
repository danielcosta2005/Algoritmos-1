
from utils import load_data, build_conflict_masks, extract_idxs
from algorithms import max_independent_set

def main():
    N, conflitos = load_data()
    conflict_masks = build_conflict_masks(N, conflitos)
    best_size, best_mask = max_independent_set(N, conflict_masks)

    escolhidos = extract_idxs(N, best_mask)

    # Saída no formato pedido
    print(best_size)
    if best_size > 0:
        print(" ".join(str(x) for x in escolhidos))
    else:
        print()  # linha em branco se nenhum duende (ou pode imprimir nada)

if __name__ == "__main__":
    main()