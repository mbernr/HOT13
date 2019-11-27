from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from local_search import *
from grasp import *
from vnd import *


inst = HotInstance("instances/0010_k2.txt")
ns = DriverOneExchange()
# ns = TourReversal()
# ns = OneBlockMove()

'''

# test grasp

sol = grasp(inst,ns,using_delta_eval=False, max_iterations=100)
print(sol)
print(sol.obj())

print()
'''



'''

# test vnd 

sol = construct_random_greedy(inst, 0.25)
print(sol)
print(sol.obj())

print()

vnd(sol, using_delta_eval=False)
print(sol)
print(sol.obj())

'''


# test delta eval

sol = construct_random_greedy(inst, 1.0)
# sol = construct_greedy(inst)
# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])

print(sol)
print(sol.obj())
print()

copy = sol.copy()

print("no delta")
local_search(sol, ns,
	max_iterations=100,
	step_function="best_improvement",
	using_delta_eval=False)

print(sol)
print(sol.obj())
print()

print("with delta")
local_search(copy, ns,
	max_iterations=100,
	step_function="best_improvement",
	using_delta_eval=True)

print(copy)
print(copy.obj())
print()

