from utils import load_data
from problems import prob1, prob2, prob3

g = load_data()

prob1(g, 1)

result_prob2, subgrafo = prob2(g, 1, g.num_vertices())

if result_prob2:
    print("Parte 2:", " ".join(map(str, result_prob2)))
else:
    print("Parte 2: -1")

prob3(subgrafo, 1)