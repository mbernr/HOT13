from neighbourhood_structures import*
import random
import time
import math


def simulated_annealing(sol, nsa, T, alpha = 0.95, max_iterations=1000, max_time=15*60):
	'''
		sol = initial solution
		ns = neighbourhood structure array
		T = initial temperature
		alpha = cooling rate
		max_iterations
		max_time
	'''
	starting_time = time.time()
	t = 0
	stopping_crit = False
	eq_condition = 0
	curr_sol = sol.copy()
	temp_sol = sol.copy()

	while(stopping_crit == False):
		while(eq_condition != sol.inst.n*(sol.inst.n-1)):
			temp_sol.copy_from(curr_sol)
			ns = random.choice(nsa)
			ns.move(temp_sol, "random_improvement", True)
			if temp_sol.obj() < curr_sol.obj():
				curr_sol.copy_from(temp_sol)
			else:
				prob = 1
				while prob==1:
					prob = random.uniform(0, 1)

				formula = math.exp(-(abs(temp_sol.obj() - curr_sol.obj()))/T)

				if prob < formula:
					curr_sol.copy_from(temp_sol)
			t += 1
			eq_condition += 1

		eq_condition = 0
		geometric_cooling(T, alpha)

		if max_iterations < t:
			stopping_crit = True
			print("max interations reached")
			print("current time: ", time.time()-starting_time)
		if time.time()-starting_time > max_time:
			stopping_crit = True
			print("timeout reached")
			print("iterations done: ", t)

	sol.copy_from(curr_sol)

def geometric_cooling(T, alpha):
	return T * alpha