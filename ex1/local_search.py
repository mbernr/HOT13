import math
import time

def local_search(sol, ns, max_iterations=math.inf, max_time=math.inf, step_function="best_improve", using_delta_eval=True):
	
	iterations = 0
	start_time = time.time()
	
	while ns.move(sol, step_function=step_function, using_delta_eval=using_delta_eval):

		print(sol)
		print(sol.obj())
		print()

		# checking if max number of iterations is exceeded
		iterations += 1
		if iterations >= max_iterations:
			break

		# checking if max time is exceeded
		if time.time()-start_time > max_time:
			break
