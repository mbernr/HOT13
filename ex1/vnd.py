import math
import time
from neighbourhood_structures import *


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

