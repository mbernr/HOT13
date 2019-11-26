import numpy as np
import random


class TourReversal:

	def apply(self, sol, p1, p2):
		sol.tour = self.reverse_array_section(sol.tour, p1,p2)
		sol.drivers = self.reverse_array_section(sol.drivers, p1,p2)

	def move(self, sol, step_function="best_improvement", using_delta_eval=False):
		if step_function == "random_improvement":
			pos1 = random.randint(0,sol.inst.n-1)
			pos2 = random.randint(0,sol.inst.n-1)
			self.apply(sol, pos1, pos2)
			return True
		else:
			best_so_far = sol
			for pos1 in range(sol.inst.n):
				for pos2 in range(pos1+1, sol.inst.n):
					if using_delta_eval:
						pass
					else:
						neighbour_solution = sol.copy()
						self.apply(neighbour_solution, pos1, pos2)
						#if neighbour_solution.is_better(best_so_far):
						if neighbour_solution.calc_objective() < best_so_far.calc_objective():
							if step_function == "next_improvement":
								self.apply(sol, pos1, pos2)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != sol:
				sol.copy_from(best_so_far)
				return True
		return False

	def delta_eval(self, sol, pos1, pos2):
		pass

	def reverse_array_section(self, array, p1, p2):
		i = min(p1, p2)
		j = max(p1, p2)
		before = array[:i]
		middle = np.flip(array[i:j+1])
		after = array[j+1:]
		return np.concatenate((before, middle, after))


class DriverOneExchange:

	def apply(self, sol, pos, driver):
		sol.drivers[pos] = driver

	def move(self, sol, step_function="best_improvement", using_delta_eval=True):
		if step_function == "random_improvement":
			pos = random.randint(0, sol.inst.n-1)
			driver = random.randint(0, sol.inst.k-1)
			self.apply(sol, pos, driver)
			return True
		else:
			best_so_far = sol
			for pos in range(sol.inst.n):
				for driver in range(sol.inst.k):
					if using_delta_eval:
						pass
					else:
						neighbour_solution = sol.copy()
						self.apply(neighbour_solution, pos,driver)
						#if neighbour_solution.is_better(best_so_far):
						if neighbour_solution.calc_objective() < best_so_far.calc_objective():
							if step_function == "next_improvement":
								self.apply(sol, pos, driver)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != sol:
				sol.copy_from(best_so_far)
				return True
		return False

	def delta_eval(self, sol, pos, driver):
		pass

class OneBlockMove:

	#moves a block from old position to new position. Everything else gets swifted accordingly to make room for it
	def apply(self, sol, old_pos, new_pos):
		if old_pos == new_pos:
			print("old_pos and new_pos are the same")

		if old_pos > new_pos:
			size = len(sol.tour)
			temp = np.zeros(size)

			for i in range(new_pos-1):
				temp[i] = sol.tour[i]

			temp[new_pos] = sol.tour[old_pos]

			for i in range(old_pos - new_pos):
				temp[new_pos + i + 1] = sol.tour[new_pos + i]

			for i in range(size - old_pos):
				temp[old_pos + i] = sol.tour[old_pos + i]

		if old_pos < new_pos:
			size = len(sol.tour)
			temp = np.zeros(size)

			for i in range(old_pos-1):
				temp[i] = sol.tour[i]

			for i in range(new_pos - old_pos):
				temp[old_pos + i] = sol.tour[old_pos + i + 1]

			temp[new_pos] = sol.tour[old_pos]

			for i in range(size - new_pos):
				temp[new_pos + i] = sol.tour[new_pos + i]


	def move(self, sol, step_function="best_improvement", using_delta_eval=True):
		if step_function == "random_improvement":
			old_pos = random.randint(0, sol.inst.n-1)
			new_pos = random.randint(0, sol.inst.n-1)
			self.apply(sol, old_pos, new_pos)
			return True
		else:
			best_so_far = sol
			for old_pos in range(sol.inst.n):
				for new_pos in range(sol.inst.n):
					if using_delta_eval:
						pass
					else:
						neighbour_solution = sol.copy()
						self.apply(neighbour_solution, old_pos, new_pos)
						#if neighbour_solution.is_better(best_so_far):
						if neighbour_solution.calc_objective() < best_so_far.calc_objective():
							if step_function == "next_improvement":
								self.apply(sol, old_pos, new_pos)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != sol:
				sol.copy_from(best_so_far)
				return True
		return False

	def delta_eval(self, sol, old_pos, new_pos):
		pass


