from utils import load_data
from problems import prob1, prob2, prob3

g = load_data()

prob1(g, 1)
prob2(g, 1, g.num_vertices())
prob3(g, 1, g.num_vertices())