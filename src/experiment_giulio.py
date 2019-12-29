from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
from ga import *
import time


start_time = time.time()


inst = HotInstance("instances/0010_k2.txt")
# ns = DriverOneExchange()
# ns = TourReversal()
# ns = OneBlockMove()


hof = ga(inst, num_generations=100, 
   pop_size=100, 
   hof_size=1,
   repl_ratio=1.0, 
   using_grasp=False,
   alpha=1.0,
   max_time=100
   )

print(hof)




# test ga
'''
hof = ga(inst, num_generations=10,
   pop_size=100, 
   hof_size=10,
   repl_ratio=1.0, 
   using_grasp=False,
   alpha=1.0)

for sol in hof:
	print(round(sol.rmse(),4))
'''


'''

# test construction

sol = construct_greedy(inst)
# sol = construct_random_greedy(inst, 0.5)
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


'''

# test local search

for ns in [TourReversal(), OneBlockMove(), DriverOneExchange()]:

	print(ns)

	for inst_name in ['0030_k2.txt', 'berlin52_k5_2.txt', 'a280_k5_1.txt']:

		inst = HotInstance("instances/" + inst_name)

		# sol = construct_random_greedy(inst, 1.0)
		sol = construct_greedy(inst)
		# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])

		print(inst_name, end = " ")

		local_search(sol, ns,
			max_time=10*60,
			step_function="best_improvement",
			using_delta_eval=True)

'''


'''

# test delta eval

for ns in [TourReversal(), OneBlockMove(), DriverOneExchange()]:

	print(ns)

	for inst_name in ['0030_k2.txt', 'berlin52_k5_2.txt', 'a280_k5_1.txt']:

		inst = HotInstance("instances/" + inst_name)

		# sol = construct_random_greedy(inst, 1.0)
		sol = construct_greedy(inst)
		# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])
		copy = sol.copy()

		no_delta_start_time = time.process_time()

		local_search(sol, ns,
			max_time=10*60,
			step_function="best_improvement",
			using_delta_eval=False)

		no_delta_time = time.process_time() - no_delta_start_time

		delta_start_time = time.process_time()

		local_search(copy, ns,
			max_time=10*60,
			step_function="best_improvement",
			using_delta_eval=True)

		delta_time = time.process_time() - delta_start_time

		print("{}, {}s, {}s".format(inst_name, no_delta_time, delta_time))

'''



print("runtime: {}".format(time.time()-start_time))
