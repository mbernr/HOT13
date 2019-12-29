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
GENNR = 1000
POPSIZE = 100
TOURSIZE = 3
CROSSOVERP=0.7  
SELECR=0.5 
MUTATIONP=0.3 

#----------------------------------------------
REPLRATIO = 0.8 
HOFSIZE = 10

GRASPIT = 10
MAXITVND = 100
TIMELIMITVND = 60*3
#------------------------------------------------

inst_list = [
	'0020_k2.txt',
	'berlin52_k1_2.txt',
	'pr439_k4_2.txt'
]


for inst_name in inst_list:
	inst_path = "instances2/" + inst_name
	inst = HotInstance(inst_path)

	print(inst_path)
	for test_param in [10, 100, 1000]: #<------- change this to modify the parameter values
		starting_time = time.process_time()
		hofscores = []
		for _ in range(10):
			hof = ga(inst, num_generations=test_param, #<----- reset the correct parameter name for the already tested parameters
				   pop_size=POPSIZE, 
				   hof_size=HOFSIZE,
				   tour_size=TOURSIZE,
				   repl_ratio=REPLRATIO, 
				   selec_ratio=SELECR,
				   crossover_prob=CROSSOVERP,
				   mutation_prob=MUTATIONP,
				   using_grasp=False
				   )

			for sol in hof:
				hofscores.append(round(sol.rmse(),4))

		hofscores = np.array(hofscores)
		mean = round(np.mean(hofscores),4)
		std = round(np.std(hofscores),4)
		running_time = round(time.process_time() - starting_time, 3)

		toprint = str(test_param) + "| best: " + str(hofscores[0]) + " mean: " + str(mean) + "std: " + str(std) + " | " + str(running_time) + "s"

		file = open("ptesting/num_generation_testing.txt", "w")  #<--------change this name to be meaningful to the parameter we are testing
		file.write(str(toprint))
		file.close()
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
