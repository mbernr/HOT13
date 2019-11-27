from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from local_search import *
from grasp import *

inst = HotInstance("instances/0010_k2.txt")
# ns = DriverOneExchange()
ns = TourReversal()

'''
sol = grasp(inst,ns,using_delta_eval=False)
print(sol)
print(sol.obj())
'''


sol = construct_random_greedy(inst, 1.0)
# sol = construct_greedy(inst)
# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])

print(sol)
print(sol.obj())
print()

# best_improvement, next_improvement, random_improvement
local_search(sol, ns, 
	max_iterations=10, 
	step_function="best_improvement", 
	using_delta_eval=False)

print(sol)
print(sol.obj())
print()


