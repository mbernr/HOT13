from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from local_search import *


inst = HotInstance("instances/0010_k2.txt")
sol = construct_greedy(inst)
ns = DriverOneExchange()

print(sol)
print(round(sol.calc_objective(),2))
print()

# best_improvement, next_improvement, random_improvement
local_search(sol, ns, max_time=1, step_function="random_improvement", using_delta_eval=False)


print(sol)
print(round(sol.obj_val,2))
print(round(sol.calc_objective(),2))
print()


'''
print(i.k, i.L, i.n, i.m)
print(i.G.edges().data())

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
'''