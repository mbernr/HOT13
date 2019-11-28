from neighbourhood_structures import *
import random
import time
import math


def local_search(sol, ns, max_iterations=math.inf, max_time=math.inf, step_function="best_improve", using_delta_eval=True):

	if step_function not in ["best_improvement", "next_improvement", "random_improvement"]:
		print("Error in local search: Invalid step function.")

	iterations = 0
	start_time = time.clock()

	while ns.move(sol, step_function=step_function, using_delta_eval=using_delta_eval):

		# checking if max number of iterations is exceeded
		iterations += 1
		if iterations >= max_iterations:
			break

		# checking if max time is exceeded
		if time.clock()-start_time > max_time:
			break


def vnd(sol, max_iterations=1000, max_time=15*60, step_function="best_improvement", using_delta_eval=True):

	if step_function not in ["best_improvement", "next_improvement", "random_improvement"]:
		print("Error in vnd: Invalid step function.")

	iterations = 0
	start_time = time.clock()

	ns = [TourReversal(), OneBlockMove(), DriverOneExchange()]
	i = 0 # index of current neighbourhood

	while(i < len(ns)):

		if ns[i].move(sol, step_function=step_function, using_delta_eval=using_delta_eval):
			i = 0
		else:
			i += 1

		iterations += 1
		if iterations >= max_iterations:
			break

		if time.clock()-start_time > max_time:
			break

def simulated_annealing(sol, nsa, T, alpha = 0.95, max_iterations=100000, max_time=15*60):
	'''
		sol = initial solution
		ns = neighbourhood structure array
		T = initial temperature
		alpha = cooling rate
		max_iterations
		max_time
	'''
	starting_time = time.clock()
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

			if time.clock()-start_time > max_time:
				break

		eq_condition = 0
		geometric_cooling(T, alpha)

		if max_iterations < t:
			stopping_crit = True
			print("max interations reached")
			print("CPU current time: ", time.clock()-starting_time)
		if time.clock()-starting_time > max_time:
			stopping_crit = True
			print("timeout reached")
			print("iterations done: ", t)

	sol.copy_from(curr_sol)

def geometric_cooling(T, alpha):
	return T * alpha