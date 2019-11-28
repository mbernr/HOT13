import time
import glob
import os

from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *


def empty_folder(path):
	files = glob.glob(path)
	for f in files:
		os.remove(f)

def store_results(sol_file_path, res_file_path, inst_name, sol, running_time, avg=-1):
	infeas = False
	if sol.is_infeasible():
		sol_file_path += "infeasible_"
		infeas = True
	solution_file = open(sol_file_path + inst_name, "w")
	solution_file.write(str(sol))
	solution_file.close()

	result_file = open(res_file_path, "a")
	result_file.write(inst_name + ", ")
	result_file.write(str(round(running_time, 4)) + "s" + ", " )
	result_file.write(str(round(sol.rmse(),4)))
	if avg != -1:
		result_file.write(", " + str(round(avg,4)))
	if infeas == True:
		result_file.write(", Solution in infeasible")
	result_file.write("\n")
	result_file.close()

print("lets go")

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
			'rl5915_k1_1.txt'].sort()

inst_list1= ['0010_k1.txt','0010_k2.txt','0015_k1.txt']


files = glob.glob('results/*')
for f in files:
	file = open(f, "w")
	file.close()

empty_folder("solutions/deterministic/*")
empty_folder("solutions/grasp/*")
empty_folder("solutions/local_search/*")
empty_folder("solutions/random/*")
empty_folder("solutions/vnd/*")
empty_folder("solutions/simulated_annealing/*")

print("the Jedi are dead")


for inst_name in inst_list1:
	inst_path = "instances/" + inst_name
	inst = HotInstance(inst_path)

	#-----------DETERMINISTIC CONSTRUCTION HEURISTIC----------------
	starting_time = time.process_time()

	det_sol = construct_greedy(inst)


	sol_file_path = "solutions/deterministic/"
	res_file_path = "results/deterministic.txt"
	running_time = time.process_time() - starting_time

	store_results(sol_file_path, res_file_path, inst_name, det_sol, running_time)

	#----------------RANDOM CONSTRUCTION HEURISTIC-----------
	starting_time = time.process_time()

	aggregate_score = 0
	nr = 10

	for i in range(nr):

		sol = construct_greedy(inst)
		if i==0:
			best_sol = sol.copy()
		else:
			if best_sol.obj() > sol.obj():
				best_sol.copy_from(sol)
		aggregate_score += sol.rmse()

	avg = aggregate_score/nr
	sol_file_path = "solutions/random/"
	res_file_path = "results/random.txt"
	running_time = time.process_time() - starting_time

	store_results(sol_file_path, res_file_path, inst_name, best_sol, running_time, avg)


	#----------------LOCAL SEARCH----------------------
	starting_time = time.process_time()
	nsa = [TourReversal(), OneBlockMove(), DriverOneExchange()]
	sfa = ["best_improvement", "next_improvement", "random"]
	max_iterations = 100
	max_time = 5

	for i in range(len(nsa)):
		for sf in sfa:
			sol.copy_from(det_sol)
			local_search(sol, nsa[i], max_iterations=max_iterations, max_time=max_time, step_function=sf, using_delta_eval=True)

			if i == 0:
				ns_name = "tour_reversal"
			if i == 1:
				ns_name = "one_block"
			if i == 2:
				ns_name = "driver_one_ex"

			sol_file_path = "solutions/local_search/" + ns_name + "_" + sf + "_"
			res_file_path = "results/local_search_"+ ns_name + "_" + sf + ".txt"
			running_time = time.process_time() - starting_time

			store_results(sol_file_path, res_file_path, inst_name, sol, running_time)

	#------------------------GRASP--------------------------
	starting_time = time.process_time()

	sol.copy_from(det_sol)
	ns = TourReversal() #TODO change to the best
	#TODO chane max_iterations and time
	sol = grasp(inst, ns, max_iterations = 100)

	sol_file_path = "solutions/grasp/"
	res_file_path = "results/grasp.txt"
	running_time = time.process_time() - starting_time

	store_results(sol_file_path, res_file_path, inst_name, sol, running_time)

	#---------------------VND----------------------

	ns_structures = [TourReversal(), OneBlockMove(), DriverOneExchange()]

	for ns_orders in [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]:

		used_ns_structures = [ns_structures[ns_orders[0]], ns_structures[ns_orders[1]], ns_structures[ns_orders[2]]]

		starting_time = time.process_time()

		sol.copy_from(det_sol)
		#TODO change max_iterations and time
		max_iterations = 100
		vnd(sol, used_ns_structures, max_iterations = max_iterations,  using_delta_eval=True)

		sol_file_path = "solutions/vnd/" 
		res_file_path = "results/vnd.txt"
		running_time = time.process_time() - starting_time

		store_results(sol_file_path, res_file_path, inst_name, sol, running_time)


	#----------------SIMULATED ANNEALING-----------
	starting_time = time.process_time()

	sol.copy_from(det_sol)
	nsa = [TourReversal(), OneBlockMove(), DriverOneExchange()]
	multiplier = 1  #variable to play around with temperature
	alpha = 0.95
	max_iterations = 10000
	max_time = 5
	T = sol.inst.M * sol.inst.k * multiplier #temperature

	simulated_annealing(sol, nsa, T, alpha=alpha, max_iterations=max_iterations, max_time=max_time)

	sol_file_path = "solutions/simulated_annealing/"
	res_file_path = "results/simulated_annealing.txt"
	running_time = time.process_time() - starting_time

	store_results(sol_file_path, res_file_path, inst_name, sol, running_time)


	#--------------ALL DONE----------------------
	print(inst_name, ": all done")



print("saul goodman")
