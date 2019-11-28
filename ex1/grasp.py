import math
from construction_heuristics import *
from search import *


def grasp(inst, ns, alpha=0.25, max_iterations=1000, max_time=15*60, max_iterations_local_search=math.inf, max_time_local_search=60, step_function="best_improvement", using_delta_eval=True):

	iterations = 0
	start_time = time.process_time()

	best_sol = None
	best_obj = math.inf

	while(True):

		sol = construct_random_greedy(inst, alpha)

		if time.clock()-start_time > max_time:
			break

		local_search(sol, ns,
			max_iterations=max_iterations_local_search,
			max_time=max_time_local_search,
			step_function=step_function,
			using_delta_eval=using_delta_eval)

		if sol.obj() < best_obj:
			best_sol = sol
			best_obj = sol.obj()

		iterations += 1
		if iterations >= max_iterations:
			break

		if time.process_time()-start_time > max_time:
			break

	return best_sol
