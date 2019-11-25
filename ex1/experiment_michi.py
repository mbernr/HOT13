from hot_instance import *
from hot_solution import *
from construction_heuristics import *


inst = HotInstance("instances/0010_k2.txt")

#print(i.k, i.L, i.n, i.m)
#print(i.G.edges().data())

det_sol = construct_greedy(inst)
print(det_sol)
print(round(det_sol.calc_objective(),2))

print()

rand_sol = construct_random_greedy(inst, 0.5)
print(rand_sol)
print(round(rand_sol.calc_objective(),2))

print()

rand_sol = construct_random_greedy(inst, 1.0)
print(rand_sol)
print(round(rand_sol.calc_objective(),2))