from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
import time 


start_time = time.time()


inst = HotInstance("instances/0010_k2.txt")
# ns = DriverOneExchange()
# ns = TourReversal()
# ns = OneBlockMove()




# test construction

sol = construct_greedy(inst)
# sol = construct_random_greedy(inst, 0.25)
print(sol)
print(sol.rmse())





'''

# test grasp

sol = grasp(inst,ns,max_iterations=100000, max_time=60)
print(sol)
print(sol.rmse())

print()

'''



'''

# test vnd 

sol = construct_random_greedy(inst, 0.25)
print(sol)
print(sol.obj())

print()
print(sol.inst.M)
print()

vnd(sol, [TourReversal(), OneBlockMove(), DriverOneExchange()], max_time=60)
print(sol)
print(sol.obj())

'''


'''

# test delta eval

sol = construct_random_greedy(inst, 1.0)
# sol = construct_greedy(inst)
# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])

print(sol)
print(sol.rmse())
print()

copy = sol.copy()

print("no delta")
local_search(sol, ns,
	max_iterations=100,
	step_function="best_improvement",
	using_delta_eval=False)

print(sol)
print(sol.rmse())
print()

print("with delta")
local_search(copy, ns,
	max_iterations=100,
	step_function="best_improvement",
	using_delta_eval=True)

print(copy)
print(copy.rmse())
print()

'''

'''

inst_list = ['0015_k2.txt',
			'a280_k5_2.txt',
			'0020_k2.txt',
			'0025_k2.txt',
			'1000_k1.txt',
			'a280_k3_2.txt',
			'0020_k1.txt',
			'3000_k2.txt',
			'berlin52_k4_1.txt',
			'a280_k2_2.txt',
			'a280_k2_1.txt',
			'rl5915_k2_1.txt',
			'rl5915_k4_2.txt',
			'1500_k1.txt',
			'berlin52_k4_2.txt',
			'a280_k1_2.txt',
			'3000_k1.txt',
			'2500_k1.txt',
			'a280_k3_1.txt',
			'berlin52_k1_2.txt',
			'a280_k5_1.txt',
			'berlin52_k3_2.txt',
			'0010_k2.txt',
			'0010_k1.txt',
			'a280_k4_2.txt',
			'a280_k1_1.txt',
			'rl5915_k5_2.txt',
			'rl5915_k2_2.txt',
			'berlin52_k2_1.txt',
			'rl5915_k3_2.txt',
			'2500_k2.txt',
			'rl5915_k4_1.txt',
			'berlin52_k3_1.txt',
			'rl5915_k1_2.txt',
			'rl5915_k5_1.txt',
			'0030_k2.txt',
			'1000_k2.txt',
			'2000_k2.txt',
			'2000_k1.txt',
			'berlin52_k1_1.txt',
			'berlin52_k5_2.txt',
			'0030_k1.txt',
			'a280_k4_1.txt',
			'0015_k1.txt',
			'0025_k1.txt',
			'1500_k2.txt',
			'berlin52_k5_1.txt',
			'berlin52_k2_2.txt',
			'rl5915_k3_1.txt',
			'rl5915_k1_1.txt']


inst_list.sort()

for inst_path in inst_list:

	inst = HotInstance("instances/" + inst_path)
	sol = construct_random_greedy(inst, 0.25)
	print(inst_path)
	print(sol.rmse())
	print()

'''



print("runtime: {}".format(time.time()-start_time))
