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


path = "instances2/0020_k2.txt"
#path = "instances2/berlin52_k2_1.txt"
#path = "instances2/bier127_k3_1.txt"
inst = HotInstance(path)


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



plt.plot(iteration_nr, means, label='Mean')
plt.plot(iteration_nr, bests, label='Best')
plt.xlabel('Generation number')
plt.ylabel('Score')
#plt.plot(iteration_nr, std_low)
#plt.plot(iteration_nr, std_up)
plt.fill_between(iteration_nr, std_low, std_up, alpha=.2)
plt.show()


print("runtime: {}".format(time.time()-start_time))
