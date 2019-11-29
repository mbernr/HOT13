from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
import time 


start_time = time.time()


# inst = HotInstance("instances/berlin52_k5_1.txt")
# ns = DriverOneExchange()
# ns = TourReversal()
# ns = OneBlockMove()


'''

# test construction

sol = construct_greedy(inst)
# sol = construct_random_greedy(inst, 0.25)
print(sol)
print(sol.rmse())

'''



'''

# test grasp

sol = grasp(inst,ns,max_iterations=100000, max_time=60)
print(sol)
print(sol.rmse())

print()

'''





# test vnd 

print("TourReversal = 0, OneBlockMove = 1, DriverOneExchange = 2")
print()


for inst_name in ['a280_k5_1.txt']:

	print(inst_name)

	inst = HotInstance("instances/" + inst_name)
	sol = construct_greedy(inst)

	ns_structures = [TourReversal(), OneBlockMove(), DriverOneExchange()]

	for ns_order in [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]:

		starting_time = time.process_time()

		used_ns_structures = [ns_structures[ns_order[0]], ns_structures[ns_order[1]], ns_structures[ns_order[2]]]
		copy = sol.copy()
		vnd(copy, used_ns_structures, max_time=60*10)

		running_time = time.process_time() - starting_time

		print("{}, {}, {}s".format(
			ns_order,
			round(copy.rmse(), 4),
			round(running_time, 4)
		))

	print()



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



print("runtime: {}".format(time.time()-start_time))
