from problems import parte1
from utils import load_data

N, blocos, Z, arvores = load_data()

altura = parte1(N, blocos)

print(f"Parte 1: {altura}")


