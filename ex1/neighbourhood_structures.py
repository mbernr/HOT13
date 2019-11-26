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
		print("old solution: ")
		if old_pos == new_pos:
			print("old_pos and new_pos are the same")
		else:
			if old_pos > new_pos:
				print("new<old")
				size = len(sol.tour)

				temp_tour = sol.tour[:new_pos]
				#print(temp_tour)
				temp_tour = np.append(temp_tour, sol.tour[old_pos])
				#print(temp_tour)
				temp_tour = np.append(temp_tour, sol.tour[(new_pos):(old_pos)])
				#print(temp_tour)
				if old_pos!=size:
					temp_tour = np.append(temp_tour, sol.tour[(old_pos + 1):])
					#print(temp_tour)

				temp_drivers = sol.drivers[:new_pos]
				temp_drivers = np.append(temp_drivers, sol.drivers[old_pos])
				temp_drivers = np.append(temp_drivers, sol.drivers[(new_pos):(old_pos)])
				temp_drivers = np.append(temp_drivers, sol.drivers[(old_pos + 1):])



			if old_pos < new_pos:
				print("old<new")
				size = len(sol.tour)
				temp_tour = []
				if (old_pos>0):
					temp_tour = sol.tour[:(old_pos)]
				temp_tour = np.append(temp_tour, sol.tour[(old_pos+1):(new_pos)])
				temp_tour = np.append(temp_tour, sol.tour[old_pos])
				temp_tour = np.append(temp_tour, sol.tour[(new_pos):])


				temp_drivers = sol.drivers[:(old_pos)]
				temp_drivers = np.append(temp_drivers, sol.drivers[(old_pos + 1):(new_pos)])
				temp_drivers = np.append(temp_drivers, sol.drivers[old_pos])
				temp_drivers = np.append(temp_drivers, sol.drivers[(new_pos):])


			sol.tour = temp_tour
			sol.drivers = temp_drivers
			sol.calc_objective()
			#self.delta_eval(sol, old_pos, new_pos)

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
		squared_error = (sol.obj_val**2)*sol.inst.k
		driver_distances = np.copy(sol.driver_distances)
		print("sol: ", sol)
		print("old_pos: ", old_pos)
		print("new_pos: ", new_pos)

		#1
		dr = sol.drivers[old_pos]
		print("dr: ", dr)
		squared_error -= driver_distances[dr]**2
		edge_weight = sol.inst.get_distance(sol.tour[old_pos], sol.tour[(new_pos+1)%sol.inst.n])
		driver_distances[dr] -= edge_weight
		squared_error += driver_distances[dr]**2

		#2
		dr = sol.drivers[(old_pos-1)%sol.inst.n]
		squared_error -= driver_distances[dr]**2
		edge_weight = sol.inst.get_distance(sol.tour[(old_pos-1)%sol.inst.n], sol.tour[(old_pos+1)%sol.inst.n])
		driver_distances[dr] -= edge_weight
		squared_error += driver_distances[dr]**2



		#3
		dr = sol.drivers[(new_pos-1)%sol.inst.n]
		squared_error -= driver_distances[dr]**2
		edge_weight = sol.inst.get_distance(sol.tour[(new_pos-1)%sol.inst.n], sol.tour[old_pos])
		driver_distances[dr] -= edge_weight
		squared_error += driver_distances[dr]**2

		eval = math.sqrt(squared_error / sol.inst.k)
		return eval

