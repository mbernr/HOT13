import time
import glob
import os
import webbrowser

from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
from ga import *
import time

#-----------------PARAMETERS TO TEST------------------
GENNR = 1000
POPSIZE = 100
TOURSIZE = 3
CROSSOVERP=0.7  
SELECR=0.5 
MUTATIONP=0.3 
ALPHAGRASP = 0.75
ALPHAVND = 1.0
#----------------------------------------------
REPLRATIO = 0.8 
HOFSIZE = 3

GRASPIT = 10
MAXITVND = 100
TIMELIMITVND = 60*3
#------------------------------------------------


def empty_folder(path):
	files = glob.glob(path)
	for f in files:
		os.remove(f)

def store_results(sol_file_path, res_file_path, inst_name, sol, running_time, avg=-1, std=-1):
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
	if std != -1:
		result_file.write(", " + str(round(std,4)))
	if infeas == True:
		result_file.write(", infeasible")
	result_file.write("\n")
	result_file.close()

print("starting..")

webbrowser.open('https://www.youtube.com/watch?v=pyCGEHYvgsU')

inst_list = [
	'0020_k1.txt', '0020_k2.txt',
	#'0100_k1.txt', '0100_k2.txt',
	#'a280_k3_1.txt', 'a280_k3_2.txt',
	#'berlin52_k1_1.txt', 'berlin52_k1_2.txt',
	#'berlin52_k2_1.txt', 'berlin52_k2_2.txt',
	#'bier127_k3_1.txt', 'bier127_k3_2.txt',
	#'pr152_k2_2.txt', 
	#'pr439_k4_1.txt', 'pr439_k4_2.txt'
]

files = glob.glob('results2/*')
for f in files:
	file = open(f, "w")
	file.close()

empty_folder("solutions2/ga_grasp/*")
empty_folder("solutions2/ga_vnd/*")

print("Folders have been cleaned. Forrest is now ready to run")

start_time = time.time()
inst = HotInstance("instances/0010_k2.txt")


for inst_name in inst_list:
	inst_path = "instances2/" + inst_name
	inst = HotInstance(inst_path)

#----------------GA using grasp to generate first generation, returning best result-------------------------
	print("GA using grasp to generate first generation")
	timegrasp = time.process_time()

	hof = ga(inst, num_generations=GENNR, 
	   pop_size=POPSIZE, 
	   hof_size=HOFSIZE,
	   tour_size=TOURSIZE,
	   repl_ratio=REPLRATIO, 
	   selection_ratio=SELECR,
	   crossover_prob=CROSSOVERP,
	   mutation_prob=MUTATIONP,
	   using_grasp=True,
	   grasp_iterations=GRASPIT,
	   alpha=ALPHAGRASP)

	print(hof[0])

	sol_file_path = "solutions2/ga_grasp/"
	res_file_path = "results2/ga_grasp.txt"
	running_time = time.process_time() - timegrasp

	store_results(sol_file_path, res_file_path, inst_name, hof[0], running_time)


#-------------ga and then plugging the 10 best in vnd, then returning best of the resulting------------------ 
	print("ga and then plugging the 10 best in vnd, then returning best of the resulting")
	timevnd = time.process_time()
	
	hof = ga(inst, num_generations=GENNR, 
	   pop_size=POPSIZE, 
	   hof_size=HOFSIZE,
	   tour_size=TOURSIZE,
	   repl_ratio=REPLRATIO, 
	   selection_ratio=SELECR,
	   crossover_prob=CROSSOVERP,
	   mutation_prob=MUTATIONP,
	   using_grasp=False,
	   alpha=ALPHAVND)

	best_pos = -1
	best_rmse = math.inf

	for i in range(len(hof)):	
		print(i)
		vnd(hof[i], [TourReversal(),  DriverOneExchange(), OneBlockMove()], max_iterations = MAXITVND,  max_time=TIMELIMITVND, using_delta_eval=True)	
		if hof[i].rmse() < best_rmse:
			best_pos = i
			best_rmse = hof[i].rmse()

	print(hof[best_pos])

	sol_file_path = "solutions2/ga_vnd/"
	res_file_path = "results2/ga_vnd.txt"
	running_time = time.process_time() - timevnd

	store_results(sol_file_path, res_file_path, inst_name, hof[best_pos], running_time)

	print("runtime: {}".format(time.process_time()-timevnd))

print(inst_name, ": all done")
print("time: ", round((time.time() - start_time)/60, 2), "min")
print("saul goodman")
