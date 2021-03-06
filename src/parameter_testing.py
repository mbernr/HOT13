import time
import glob
import os
import webbrowser

import numpy as np

from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from search import *
from grasp import *
from ga import *
import time

#-----------------PARAMETERS TO TEST------------------ <---- update them here once you run them
GENNR = 200 # this, or 500, or 1000 with time limit
POPSIZE = 100 # this, or 200
TOURSIZE = 5 # actually doesn't really make a performance difference, 5 is fine
SELECR=0.25 # sweet spot between run time and objective
CROSSOVERP=0.3 # this combination of probabilities is the fastest,
MUTATIONP=0.7 # with the best objective
ALPHAGRASP = 0.75
ALPHAVND = 1.0
#----------------------------------------------
REPLRATIO = 0.8 
HOFSIZE = 10

TIMELIMITGA=60*10

GRASPIT = 10
MAXITVND = 100
TIMELIMITVND = 60*3
#------------------------------------------------

inst_list = [
	'0020_k2.txt',
	'berlin52_k1_2.txt',
	'bier127_k3_1.txt',
]

for inst_name in inst_list:
	inst_path = "instances2/" + inst_name
	inst = HotInstance(inst_path)

	print(inst_path)
	
	#GA

	starting_time = time.process_time()
	hofscores = []
	num_infeas_solutions = 0
	for _ in range(10):
		hof = ga(inst, 
			   num_generations=GENNR, #<----- reset the correct parameter name for the already tested parameters
			   pop_size=POPSIZE, 
			   hof_size=HOFSIZE,
			   tour_size=TOURSIZE,
			   repl_ratio=REPLRATIO, 
			   selec_ratio=SELECR,
			   crossover_prob=CROSSOVERP,
			   mutation_prob=MUTATIONP,
			   using_grasp=False,
			   max_time=TIMELIMITGA
			   )

		best_pos = -1
		best_rmse = math.inf

		#for i in range(len(hof)):	
		#	vnd(hof[i], [TourReversal(),  DriverOneExchange(), OneBlockMove()], max_iterations = MAXITVND,  max_time=TIMELIMITVND, using_delta_eval=True)	
		#	if hof[i].rmse() < best_rmse:
		#		best_pos = i
		#		best_rmse = hof[i].rmse()

		for sol in hof:
			hofscores.append(round(sol.rmse(),4))
			if sol.is_infeasible():
				num_infeas_solutions += 1

	hofscores = np.sort(np.array(hofscores))
	mean = round(np.mean(hofscores),4)
	std = round(np.std(hofscores),4)
	running_time = round(time.process_time() - starting_time, 3)

	toprint = "best: " + str(hofscores[0]) + ", mean: " + str(mean) + ", std: " + str(std) + ", infeas: " + str(num_infeas_solutions)+"/"+str(len(hofscores)) + " | " + str(running_time) + "s"

	# file = open("ptesting/num_generation_testing.txt", "w")  #<-------- I uncommented this, cause it was not working properly
	# file.write(str(toprint))
	# file.close()
	print("naked GA")
	print(toprint)

	print()
#GRASP
	starting_time = time.process_time()
	hofscores = []
	num_infeas_solutions = 0
	for _ in range(10):
		hof = ga(inst, 
			   num_generations=GENNR, #<----- reset the correct parameter name for the already tested parameters
			   pop_size=POPSIZE, 
			   hof_size=HOFSIZE,
			   tour_size=TOURSIZE,
			   repl_ratio=REPLRATIO, 
			   selec_ratio=SELECR,
			   crossover_prob=CROSSOVERP,
			   mutation_prob=MUTATIONP,
			   using_grasp=True,
			   grasp_iterations=GRASPIT,
			   alpha=ALPHAGRASP,
			   max_time=TIMELIMITGA
			   )

		best_pos = -1
		best_rmse = math.inf

		#for i in range(len(hof)):	
		#	vnd(hof[i], [TourReversal(),  DriverOneExchange(), OneBlockMove()], max_iterations = MAXITVND,  max_time=TIMELIMITVND, using_delta_eval=True)	
		#	if hof[i].rmse() < best_rmse:
		#		best_pos = i
		#		best_rmse = hof[i].rmse()

		for sol in hof:
			hofscores.append(round(sol.rmse(),4))
			if sol.is_infeasible():
				num_infeas_solutions += 1

	hofscores = np.sort(np.array(hofscores))
	mean = round(np.mean(hofscores),4)
	std = round(np.std(hofscores),4)
	running_time = round(time.process_time() - starting_time, 3)

	toprint = "best: " + str(hofscores[0]) + ", mean: " + str(mean) + ", std: " + str(std) + ", infeas: " + str(num_infeas_solutions)+"/"+str(len(hofscores)) + " | " + str(running_time) + "s"

	# file = open("ptesting/num_generation_testing.txt", "w")  #<-------- I uncommented this, cause it was not working properly
	# file.write(str(toprint))
	# file.close()

	print("GRASP")
	print(toprint)

	print()
#VND
	starting_time = time.process_time()
	hofscores = []
	num_infeas_solutions = 0
	for _ in range(10):
		hof = ga(inst, 
			   num_generations=GENNR, #<----- reset the correct parameter name for the already tested parameters
			   pop_size=POPSIZE, 
			   hof_size=HOFSIZE,
			   tour_size=TOURSIZE,
			   repl_ratio=REPLRATIO, 
			   selec_ratio=SELECR,
			   crossover_prob=CROSSOVERP,
			   mutation_prob=MUTATIONP,
			   using_grasp=False,
			   max_time=TIMELIMITGA
			   )

		best_pos = -1
		best_rmse = math.inf

		for i in range(len(hof)):	
			vnd(hof[i], [TourReversal(),  DriverOneExchange(), OneBlockMove()], max_iterations = MAXITVND,  max_time=TIMELIMITVND, using_delta_eval=True)	
			if hof[i].rmse() < best_rmse:
				best_pos = i
				best_rmse = hof[i].rmse()

		for sol in hof:
			hofscores.append(round(sol.rmse(),4))
			if sol.is_infeasible():
				num_infeas_solutions += 1

	hofscores = np.sort(np.array(hofscores))
	mean = round(np.mean(hofscores),4)
	std = round(np.std(hofscores),4)
	running_time = round(time.process_time() - starting_time, 3)

	toprint = "best: " + str(hofscores[0]) + ", mean: " + str(mean) + ", std: " + str(std) + ", infeas: " + str(num_infeas_solutions)+"/"+str(len(hofscores)) + " | " + str(running_time) + "s"

	# file = open("ptesting/num_generation_testing.txt", "w")  #<-------- I uncommented this, cause it was not working properly
	# file.write(str(toprint))
	# file.close()
	print("VND")
	print(toprint)

	print()
'''
TO USE:
1. change name of the file so that we know what we are doing
2. change the parameter values taht you want to test
3. change the parameter in the GA call
4. run the thing
5. update the paramenters at the top of the file so we later on the runs have better parameters
'''
