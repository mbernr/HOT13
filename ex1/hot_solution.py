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
			self.tour = np.array(tour)
		else:
			self.tour = np.array([i for i in range(inst.n)])

		if len(drivers) > 0:
			self.drivers = np.array(drivers)
		else:
			self.drivers = np.zeros(self.inst.n, dtype=int)

		self.calc_objective()


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
		s = ""
		for vertex in self.tour:
			s += str(vertex) + " "
		s += "\n "
		for driver in self.drivers:
			s += str(driver) + " "
		return s


	def calc_objective(self):
		self.calc_driver_distances()
		squared_error_per_driver = np.square(self.driver_distances)
		squared_error = np.sum(squared_error_per_driver)
		self.obj_val = sqrt((1/self.inst.k)*squared_error)
		self.obj_val_valid = True
		return self.obj_val


	def calc_driver_distances(self):
		k = self.inst.k
		n = self.inst.n
		L = self.inst.L
		self.driver_distances = np.full(k, -L)
		for i in range(n-1):
			driver = self.drivers[i]
			dist = self.inst.get_distance(self.tour[i], self.tour[i+1])
			self.driver_distances[driver] += dist
		driver = self.drivers[n-1]
		dist = self.inst.get_distance(self.tour[n-1], self.tour[0])
		self.driver_distances[driver] += dist


	def initialize(self, k):
		print("---- used initialized ----")
		pass

	def __eq__(self, other):
		if self.inst == other.inst and (self.tour == other.tour).all() and (self.drivers == other.drivers).all():
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