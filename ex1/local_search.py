import math
import time

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
