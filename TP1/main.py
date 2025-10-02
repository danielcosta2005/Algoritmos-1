from utils import load_data
from algorithms import prob1
from algorithms import prob2

g = load_data()

prob1(g, 1)
prob2(g, 1, g.num_vertices())