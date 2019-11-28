import numpy as np
import random
import math


class TourReversal:

	def apply(self, sol, p1, p2):
		if p1 == p2 or abs(p1-p2) == (sol.inst.n-1):
			return
		else:
			p1, p2 = min(p1, p2), max(p1, p2)
			sol.tour = self.reverse_array_section(sol.tour, p1,p2)
			sol.drivers = self.reverse_array_section(sol.drivers, p1, p2-1)
			sol.calc_objective()

	def move(self, sol, step_function="best_improvement", using_delta_eval=False):
		if step_function == "random":
			pos1 = random.randint(0,sol.inst.n-1)
			pos2 = random.randint(0,sol.inst.n-1)
			self.apply(sol, pos1, pos2)
			return True
		else:
			best = {"obj": sol.obj(), "pos1": -1, "pos2": -1}
			for pos1 in range(sol.inst.n):
				for pos2 in range(pos1+1, sol.inst.n):
					if pos1 == pos2 or abs(pos1-pos2) == (sol.inst.n-1):
						continue
					if using_delta_eval:
						neighbour_obj = self.delta_eval(sol, pos1, pos2)
					else:
						neighbour_solution = sol.copy()
						self.apply(neighbour_solution, pos1,pos2)
						neighbour_obj = neighbour_solution.obj()
					if neighbour_obj < best["obj"]:
						if step_function == "next_improvement":
							self.apply(sol, pos1, pos2)
							return True
						elif step_function == "best_improvement":
							best["pos1"] = pos1
							best["pos2"] = pos2
							best["obj"] = neighbour_obj
			if best["pos1"] >= 0 and best["pos2"] >= 0:
				self.apply(sol, best["pos1"], best["pos2"])
				return True
		return False

	def delta_eval(self, sol, pos1, pos2):

		if pos1 == pos2 or abs(pos1-pos2) == (sol.inst.n-1) :
			return sol.obj()
		else:
			pos1, pos2 = min(pos1, pos2), max(pos1, pos2)

			squared_error = sol.obj()
			driver_distances = np.copy(sol.driver_distances)

			#1
			dr = sol.drivers[(pos1-1)%sol.inst.n]
			edge_to_remove_dist = sol.inst.get_distance(sol.tour[(pos1-1)%sol.inst.n], sol.tour[pos1])
			edge_to_add_dist = sol.inst.get_distance(sol.tour[(pos1-1)%sol.inst.n], sol.tour[pos2])
			squared_error = replace_one_edge(squared_error, driver_distances, dr, edge_to_remove_dist, edge_to_add_dist)

			#2
			dr = sol.drivers[pos2]
			edge_to_remove_dist = sol.inst.get_distance(sol.tour[pos2], sol.tour[(pos2+1)%sol.inst.n])
			edge_to_add_dist = sol.inst.get_distance(sol.tour[pos1], sol.tour[(pos2+1)%sol.inst.n])
			squared_error = replace_one_edge(squared_error, driver_distances, dr, edge_to_remove_dist, edge_to_add_dist)

			return squared_error

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
		if step_function == "random":
			pos = random.randint(0, sol.inst.n-1)
			driver = random.randint(0, sol.inst.k-1)
			self.apply(sol, pos, driver)
			return True
		else:
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
		if sol.drivers[pos] == new_driver:
			return sol.obj()
		driver_distances = np.copy(sol.driver_distances)
		squared_error = sol.obj()
		old_driver = sol.drivers[pos]
		edge_weight = sol.inst.get_distance(sol.tour[pos], sol.tour[(pos+1)%sol.inst.n])
		squared_error -= driver_distances[old_driver]**2
		squared_error -= driver_distances[new_driver]**2
		driver_distances[old_driver] -= edge_weight
		driver_distances[new_driver] += edge_weight
		squared_error += driver_distances[old_driver]**2
		squared_error += driver_distances[new_driver]**2
		return squared_error


class OneBlockMove:

	#moves a block from old position to new position. Everything else gets swifted accordingly to make room for it
	def apply(self, sol, old_pos, new_pos):
		if old_pos == new_pos or  abs(old_pos - new_pos) == (sol.inst.n-1):
			pass
		elif abs(old_pos - new_pos) == 1:
			tr = TourReversal()
			tr.apply(sol, old_pos, new_pos)
		else:
			if old_pos > new_pos:
				size = len(sol.tour)

				temp_tour = sol.tour[:new_pos]
				temp_tour = np.append(temp_tour, sol.tour[old_pos])
				temp_tour = np.append(temp_tour, sol.tour[(new_pos):(old_pos)])
				if old_pos!=size:
					temp_tour = np.append(temp_tour, sol.tour[(old_pos + 1):])

				temp_drivers = sol.drivers[:new_pos]
				temp_drivers = np.append(temp_drivers, sol.drivers[old_pos])
				temp_drivers = np.append(temp_drivers, sol.drivers[(new_pos):(old_pos)])
				temp_drivers = np.append(temp_drivers, sol.drivers[(old_pos + 1):])


			if old_pos < new_pos:
				size = len(sol.tour)

				temp_tour = np.empty(0, int)
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

	def move(self, sol, step_function="best_improvement", using_delta_eval=True):

		if step_function == "random":
			old_pos = random.randint(0, sol.inst.n-1)
			new_pos = random.randint(0, sol.inst.n-1)
			self.apply(sol, old_pos, new_pos)
			return True
		else:
			best = {"obj": sol.obj(), "old_pos": -1, "new_pos": -1}
			for old_pos in range(sol.inst.n):
				for new_pos in range(sol.inst.n):
					if old_pos == new_pos or  abs(old_pos - new_pos) == (sol.inst.n-1):
						continue
					if using_delta_eval:
						neighbour_obj = self.delta_eval(sol, old_pos, new_pos)
					else:
						neighbour_solution = sol.copy()
						self.apply(neighbour_solution, old_pos, new_pos)
						neighbour_obj = neighbour_solution.obj()
					if neighbour_obj < best["obj"]:
						if step_function == "next_improvement":
							self.apply(sol, old_pos, new_pos)
							return True
						elif step_function == "best_improvement":
							best["obj"] = neighbour_obj
							best["old_pos"] = old_pos
							best["new_pos"] = new_pos
			if best["old_pos"] >=0 and best["new_pos"] >= 0:
				self.apply(sol, best["old_pos"], best["new_pos"])
				return True
		return False

	def delta_eval(self, sol, old_pos, new_pos):
		if old_pos == new_pos:
			return sol.obj()

		else:
			if abs(old_pos - new_pos) == 1 or abs(old_pos - new_pos) == (sol.inst.n-1):
				tr = TourReversal()
				return tr.delta_eval(sol, old_pos, new_pos)
			else:
				squared_error = sol.obj()
				driver_distances = np.copy(sol.driver_distances)

				#1
				dr = sol.drivers[old_pos]
				edge_to_remove_dist = sol.inst.get_distance(sol.tour[old_pos], sol.tour[(old_pos+1)%sol.inst.n])
				edge_to_add_dist = sol.inst.get_distance(sol.tour[old_pos], sol.tour[new_pos])
				squared_error = replace_one_edge(squared_error, driver_distances, dr, edge_to_remove_dist, edge_to_add_dist)

				#2
				dr = sol.drivers[(old_pos-1)%sol.inst.n]
				edge_to_remove_dist = sol.inst.get_distance(sol.tour[(old_pos-1)%sol.inst.n], sol.tour[old_pos])
				edge_to_add_dist = sol.inst.get_distance(sol.tour[(old_pos-1)%sol.inst.n], sol.tour[(old_pos+1)%sol.inst.n])
				squared_error = replace_one_edge(squared_error, driver_distances, dr, edge_to_remove_dist, edge_to_add_dist)

				#3
				dr = sol.drivers[(new_pos-1)%sol.inst.n]
				edge_to_remove_dist = sol.inst.get_distance(sol.tour[(new_pos-1)%sol.inst.n], sol.tour[new_pos])
				edge_to_add_dist = sol.inst.get_distance(sol.tour[(new_pos-1)%sol.inst.n], sol.tour[old_pos])
				squared_error = replace_one_edge(squared_error, driver_distances, dr, edge_to_remove_dist, edge_to_add_dist)

				return squared_error

def replace_one_edge(squared_error, driver_distances, dr, edge_to_remove_dist, edge_to_add_dist):
	squared_error -= driver_distances[dr]**2
	driver_distances[dr] -= edge_to_remove_dist
	driver_distances[dr] += edge_to_add_dist
	squared_error += driver_distances[dr]**2
	return squared_error
