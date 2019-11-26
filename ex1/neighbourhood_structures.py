import numpy as np
import random
import math


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
		sol.calc_objective()

	def move(self, sol, step_function="best_improvement", using_delta_eval=True):
		if step_function == "random_improvement":
			pos = random.randint(0, sol.inst.n-1)
			driver = random.randint(0, sol.inst.k-1)
			self.apply(sol, pos, driver)
			return True
		else:
			best_so_far = sol
			best = {"obj": sol.obj(), "pos": -1, "driver": -1}
			for pos in range(sol.inst.n):
				for driver in range(sol.inst.k):
					if sol.drivers[pos] == driver:
						continue
					if using_delta_eval:
						neighbour_obj = self.delta_eval(sol, pos, driver)
					else:
						neighbour_solution = sol.copy()
						self.apply(neighbour_solution, pos,driver)
						neighbour_obj = neighbour_solution.obj()
					if neighbour_obj < best["obj"]:
						if step_function == "next_improvement":
							self.apply(sol, pos, driver)
							return True
						elif step_function == "best_improvement":
							best["pos"] = pos
							best["driver"] = driver
							best["obj"] = neighbour_obj
			if best["pos"] >= 0 and best["driver"] >= 0:
				self.apply(sol, best["pos"], best["driver"])
				return True
		return False

	def delta_eval(self, sol, pos, new_driver):
		driver_distances = np.copy(sol.driver_distances)
		squared_error = (sol.obj_val**2)*sol.inst.k
		old_driver = sol.drivers[pos]
		edge_weight = sol.inst.get_distance(sol.tour[pos], sol.tour[(pos+1)%sol.inst.n])
		squared_error -= driver_distances[old_driver]**2
		squared_error -= driver_distances[new_driver]**2
		driver_distances[old_driver] -= edge_weight
		driver_distances[new_driver] += edge_weight
		squared_error += driver_distances[old_driver]**2
		squared_error += driver_distances[new_driver]**2
		return math.sqrt(squared_error / sol.inst.k)


class OneBlockMove:

	#moves a block from old position to new position. Everything else gets swifted accordingly to make room for it
	def apply(self, sol, old_pos, new_pos):
		if old_pos == new_pos:
			print("old_pos and new_pos are the same")
		else:
			if old_pos > new_pos:
				print("new<old")
				size = len(sol.tour)
				temp_tour = np.zeros(size)
				temp_drivers = np.zeros(size)

				for i in range(new_pos-1):
					temp_tour[i] = sol.tour[i]
					temp_drivers[i] = sol.drivers[i]

				temp_tour[new_pos] = sol.tour[old_pos]
				temp_drivers[new_pos] = sol.drivers[old_pos]

				for i in range(old_pos - new_pos):
					temp_tour[new_pos + i + 1] = sol.tour[new_pos + i]
					temp_drivers[new_pos + i + 1] = sol.drivers[new_pos + i]

				for i in range(size - old_pos):
					temp_tour[old_pos + i] = sol.tour[old_pos + i]
					temp_drivers[old_pos + i] = sol.drivers[old_pos + i]

			if old_pos < new_pos:
				print("old<new")
				size = len(sol.tour)
				temp_tour = np.zeros(size)
				temp_drivers = np.zeros(size)

				for i in range(old_pos-1):
					temp_tour[i] = sol.tour[i]
					temp_drivers[i] = sol.drivers[i]

				for i in range(new_pos - old_pos):
					temp_tour[old_pos + i] = sol.tour[old_pos + i + 1]
					temp_drivers[old_pos + i] = sol.drivers[old_pos + i + 1]

			temp_tour[new_pos] = sol.tour[old_pos]
			temp_drivers[new_pos] = sol.drivers[old_pos]

			for i in range(size - new_pos):
				temp_tour[new_pos + i] = sol.tour[new_pos + i]
				temp_drivers[new_pos + i] = sol.drivers[new_pos + i]

			sol.tour = temp_tour
			sol.drivers = temp_drivers
			self.delta_eval(sol, old_pos, new_pos)

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


