from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
from ga import *
import time
import matplotlib.pyplot as plt

start_time = time.time()

#path = "instances2/0020_k2.txt"
#path = "instances2/berlin52_k2_1.txt"
path = "instances2/bier127_k3_1.txt"

inst = HotInstance(path)

# ns = DriverOneExchange()
# ns = TourReversal()
# ns = OneBlockMove()

GENNR = 1000 # this, or 500, or 1000 with time limit
POPSIZE = 100 # this, or 200
TOURSIZE = 5 # actually doesn't really make a performance difference, 5 is fine
SELECR=0.25 # sweet spot between run time and objective
CROSSOVERP=0.3 # this combination of probabilities is the fastest,
MUTATIONP=0.7 # with the best objective
ALPHA = 1.0
#----------------------------------------------
REPLRATIO = 0.8 
HOFSIZE = 3
TIMELIMIT = 60*10



hof, gen_data = ga(inst, num_generations=GENNR, 
		   pop_size=POPSIZE, 
		   hof_size=HOFSIZE,
		   tour_size=TOURSIZE,
		   repl_ratio=REPLRATIO, 
		   selec_ratio=SELECR,
		   crossover_prob=CROSSOVERP,
		   mutation_prob=MUTATIONP,
		   using_grasp=False,
		   alpha=ALPHA,
		   max_time=TIMELIMIT,
		   return_gen_data=True
		   )


print(hof)
print(gen_data)
iteration_nr = []
bests = []
means = []
stds = []

for el in gen_data:
	iteration_nr.append(el[0])
	bests.append(el[1])
	means.append(el[2])
	stds.append(el[3])
	
std_low = []
std_up = []

for i in range(len(stds)):
	std_low.append(means[i] - stds[i])
	std_up.append(means[i] + stds[i])



plt.plot(iteration_nr, means)
plt.plot(iteration_nr, bests)

#plt.plot(iteration_nr, std_low)
#plt.plot(iteration_nr, std_up)
plt.fill_between(iteration_nr, std_low, std_up, alpha=.2)
plt.show()



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
