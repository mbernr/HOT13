from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from local_search import *
from grasp import *
from vnd import *


inst = HotInstance("instances/0010_k2.txt")
# ns = DriverOneExchange()
#ns = TourReversal()

ns = OneBlockMove()

'''
sol = grasp(inst,ns,using_delta_eval=False, max_iterations=100)
print(sol)
print(sol.obj())
'''


print()
sol = construct_random_greedy(inst, 1.0)
#sol = construct_greedy(inst)
# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])

print(sol)
print(sol.obj())
print()

print("delta")
local_search(sol, ns,
    max_iterations=10,
    step_function="best_improvement",
    using_delta_eval=True)
print(sol)
print(sol.obj())
print()

sol1 =sol.copy()
# best_improvement, next_improvement, random_improvement
print("no delta")
local_search(sol1, ns,
    max_iterations=10,
    step_function="best_improvement",
    using_delta_eval=False)

print(sol1)
print(sol1.obj())
print()
