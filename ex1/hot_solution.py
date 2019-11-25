import numpy as np
from pymhlib.solution import Solution
from math import sqrt
import copy
import random

from hot_instance import *


class HotSolution(Solution):

	def __init__(self, inst: HotInstance, tour=[], drivers=[]):
		super().__init__(inst=inst)
		self.obj_val_valid = False
		self.to_maximize = False

		if len(tour) > 0:
			self.tour = tour
		else:
			self.tour = np.array([i for i in range(inst.n)])
			
		if len(drivers) > 0:
			self.drivers = drivers
		else:
			self.drivers = np.zeros(self.inst.n, dtype=int)


	def copy(self):
		copied_tour = np.copy(self.tour)
		copied_drivers = np.copy(self.drivers)
		return HotSolution(self.inst, tour=copied_tour, drivers=copied_drivers)

	def copy_from(self, other: 'HotSolution'):
		self.tour = np.copy(other.tour)
		self.drivers = np.copy(other.drivers)
		self.inst = other.inst

	def __repr__(self): #TODO: nice representation with offset
		s = ""
		for vertex in self.tour:
			s += str(vertex) + " "
		s += "\n "
		for driver in self.drivers:
			s += str(driver) + " "
		return s

	def calc_objective(self):

		k = self.inst.k
		n = self.inst.n
		L = self.inst.L
		driver_distances = np.full(k, L)

		for i in range(n-1):
			driver = self.drivers[i]
			dist = self.inst.get_distance(self.tour[i], self.tour[i+1])
			driver_distances[driver] -= dist
		driver = self.drivers[n-1]
		dist = self.inst.get_distance(self.tour[n-1], self.tour[0])
		driver_distances[driver] -= dist

		squared_error_per_driver = np.square(driver_distances)
		squared_error = np.sum(squared_error_per_driver)
		return sqrt((1/k)*squared_error)


	def initialize(self, k):
		print("---- used initialized ----")
		pass

	def __eq__(self, other):
		if self.inst == other.inst and self.tour.all() == other.tour.all() and self.drivers.all() == other.drivers.all():
			return True
		else:
			return False

	def check(self):

		if len(self.tour) != self.inst.n:
			raise ValueError("Invalid length of tour in solution")

		if len(self.drivers) != self.inst.n:
			raise ValueError("Invalid length of drivers in solution")

		if len(self.tour) != len(set(self.tour)):
			raise ValueError("Repeated node in solution")

		if (self.tour >= self.inst.n).any():
			raise ValueError("Invalid node in solution")

		if (self.drivers >= self.inst.k).any():
			raise ValueError("Invalid driver in solution")

		super().check()

	def apply_tour_swap(self, p1, p2):
		self.tour[p1], self.tour[p2] = self.tour[p2], self.tour[p1]
		self.drivers[p1], self.drivers[p2] = self.drivers[p2], self.drivers[p1]

	def apply_driver_flip(self, pos, driver):
		self.drivers[pos] = driver

	def apply_driver_swap(self, i, j):
		self.drivers[i], self.drivers[j] = self.drivers[j], self.drivers[i]

	def neighbourhood_search_driver_flip(self, step_function="next_improvement", delta_eval=False):
		if step_function == "random":
			pos = random.randint(0,len(self.drivers))
			driver = random.randint(0,self.inst.k)
			print(pos, driver)
			self.apply_driver_flip(pos, driver)
			return True
		else:
			best_so_far = self
			for pos in range(len(self.drivers)):
				for driver in range(self.inst.k):
					if delta_eval:
						pass
					else:
						neighbour_solution = self.copy()
						neighbour_solution.apply_driver_flip(pos,driver)
						if neighbour_solution.is_better(best_so_far):
							if step_function == "next_improvement":
								self.apply_driver_flip(pos, driver)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != self:
				self.copy_from(best_so_far)
				return True
		return False

	def neighbourhood_search_driver_swap(self, step_function="next_improvement", delta_eval=False):
		if step_function == "random":
			driver1 = random.randint(0,self.inst.k)
			driver2 = random.randint(0,self.inst.k)
			self.apply_driver_swap(driver1, driver2)
			return True
		else:
			best_so_far = self
			for driver1 in self.inst.k:
				for driver2 in self.inst.k:
					if delta_eval:
						pass
					else:
						neighbour_solution = self.copy()
						neighbour_solution.apply_driver_swap(driver1,driver2)
						if neighbour_solution.is_better(best_so_far):
							if step_function == "next_improvement":
								self.apply_driver_swap(driver1, driver2)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != self:
				self.copy_from(best_so_far)
				return True
		return False


	def neighbourhood_search_tour_swap(self, step_function="next_improvement", delta_eval=False):
		if step_function == "random":
			pos1 = random.randint(0,len(self.drivers))
			pos2 = random.randint(0,len(self.drivers))
			self.apply_driver_flip(pos, driver)
			return True
		else:
			best_so_far = self
			for pos1 in range(len(self.drivers)):
				for pos2 in range(len(self.drivers)):
					if delta_eval:
						pass
					else:
						neighbour_solution = self.copy()
						neighbour_solution.apply_tour_swap(pos1, pos2)
						if neighbour_solution.is_better(best_so_far):
							if step_function == "next_improvement":
								self.apply_tour_swap(pos1, pos2)
								return True
							elif step_function == "best_improvement":
								best_so_far = neighbour_solution
			if best_so_far != self:
				self.copy_from(best_so_far)
				return True
		return False