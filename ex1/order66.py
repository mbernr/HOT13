from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
import time
import glob


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


print("all good")
