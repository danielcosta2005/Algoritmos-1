from problems import parte1, parte2
from utils import load_data

N, blocos, arvores = load_data()

altura = parte1(N, blocos)
print(f"Parte 1: {altura}")

per, i, j, k = parte2(arvores)
print(f"Parte 2: {per:.4f} {i} {j} {k}")


