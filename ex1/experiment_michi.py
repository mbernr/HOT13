from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from local_search import *
from grasp import *

inst = HotInstance("instances/0010_k2.txt")
ns = DriverOneExchange()

sol = grasp(inst,ns)
print(sol)
print(sol.obj())


'''
inst = HotInstance("instances/0010_k2.txt")
sol = construct_random_greedy(inst, 0.5)
ns = DriverOneExchange()

print(sol)
print(sol.obj())
print()

# best_improvement, next_improvement, random_improvement
local_search(sol, ns, 
	max_iterations=100, 
	step_function="next_improvement", 
	using_delta_eval=False)
'''

