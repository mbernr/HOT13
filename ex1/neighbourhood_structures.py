

class DriverOneExchange:

	def apply(self, sol, pos, driver):
		sol.drivers[pos] = driver

	def move(self, sol, step_function="next_improvement", using_delta_eval=True):
		if step_function == "random_improvement":
			pos = random.randint(0, len(sol.drivers)-1)
			driver = random.randint(0, sol.inst.k-1)
			sol.apply_driver_flip(pos, driver)
			return True
		else:
			best_so_far = sol
			for pos in range(len(sol.drivers)):
				for driver in range(sol.inst.k):
					if using_delta_eval:
						pass
					else:
						neighbour_solution = sol.copy()
						neighbour_solution.apply_driver_flip(pos,driver)
						#if neighbour_solution.is_better(best_so_far):
						if neighbour_solution.calc_objective() < best_so_far.calc_objective():
							if step_function == "next_improvement":
								sol.apply_driver_flip(pos, driver)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != sol:
				sol.copy_from(best_so_far)
				return True
		return False

	def delta_eval(self, sol, pos, driver):
		pass


