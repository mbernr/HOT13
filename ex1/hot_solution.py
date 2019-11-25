import numpy as np
from pymhlib.solution import Solution
from math import sqrt

from hot_instance import *


class HotSolution(Solution):

	def __init__(self, inst: HotInstance, tour=None, drivers=None):
		super().__init__(inst=inst)
		self.obj_val_valid = False
		self.to_maximize = False

		self.tour = np.array([i for i in range(inst.n)])
		self.drivers = np.zeros(self.inst.n, dtype=int)
		if tour != None:
			self.tour = tour
		if drivers != None:
			self.drivers = drivers
		

	def copy(self):
		copied_tour = np.array([self.tour[i] for i in range(self.inst.n)])
		copied_drivers = np.array([self.drivers[i] for i in range(self.inst.n)])
		return HotSolution(self.inst, tour=copied_tour, drivers=copied_drivers)

	def copy_from(self, other: 'HotSolution'):
		self.tour = np.array([other.tour[i] for i in range(other.inst.n)])
		self.drivers = np.array([other.drivers[i] for i in range(other.inst.n)])
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

		print()

		# set(self.tour)

		squared_error_per_driver = np.square(driver_distances)
		squared_error = np.sum(squared_error_per_driver)
		return sqrt((1/k)*squared_error)


	def initialize(self, k):
		print("---- used initialized ----")
		pass

	def __eq__(self, other):
		if self.inst == other.inst and self.tour == other.tour and self.drivers == other.drivers:
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

	def apply_driver_flip(self, edge, driver):
		self.drivers[edge] = driver

	def apply_driver_swap(self, i, j):
		self.drivers[i], self.drivers[j] = self.drivers[j], self.drivers[i]

