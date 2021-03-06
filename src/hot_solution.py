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
			self.tour = np.array(tour, dtype=np.int16)
		else:
			self.tour = np.arange(self.inst.n, dtype=np.int16)

		if len(drivers) > 0:
			self.drivers = np.array(drivers, dtype=np.int8)
		else:
			self.drivers = np.zeros(self.inst.n, dtype=np.int8)


	def copy(self):
		copied_tour = np.copy(self.tour)
		copied_drivers = np.copy(self.drivers)
		copied_sol = HotSolution(self.inst, tour=copied_tour, drivers=copied_drivers)
		return copied_sol

	def copy_from(self, other: 'HotSolution'):
		self.tour = np.copy(other.tour)
		self.drivers = np.copy(other.drivers)
		self.inst = other.inst
		self.obj_val = other.obj_val
		self.obj_val_valid = other.obj_val_valid
		self.driver_distances = other.driver_distances

	def __repr__(self): #TODO: nice representation with offset
		s = self.inst.name + "\n"
		for vertex in self.tour:
			s += str(vertex) + " "
		s += "\n "
		for driver in self.drivers:
			s += str(driver) + " "
		return s


	def calc_objective(self):
		self.calc_driver_distances()
		squared_error = 0
		for i in range(self.inst.k):
			squared_error += self.driver_distances[i]**2
		self.obj_val = squared_error
		self.obj_val_valid = True
		return self.obj_val


	def calc_driver_distances(self):
		self.driver_distances = [-self.inst.L for i in range(self.inst.k)]
		for i in range(self.inst.n-1):
			driver = self.drivers[i]
			dist = self.inst.get_distance(self.tour[i], self.tour[i+1])
			self.driver_distances[driver] += dist
		driver = self.drivers[self.inst.n-1]
		dist = self.inst.get_distance(self.tour[self.inst.n-1], self.tour[0])
		self.driver_distances[driver] += dist

	def rmse(self):
		return math.sqrt(self.obj() / self.inst.k)


	def initialize(self, k):
		print("---- used initialized ----")
		pass

	def __eq__(self, other):
		if self.inst == other.inst:
			for i in range(self.inst.n):
				if self.tour[i] != other.tour[i] or self.drivers[i] != other.drivers[i]:
					return False
				return True
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

	def is_infeasible(self):
		for i in range(self.inst.n):
			dist = self.inst.get_distance(self.tour[i], self.tour[(i+1)%self.inst.n])
			if dist >= self.inst.M:
				return True
		return False