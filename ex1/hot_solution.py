from pymhlib.solution import Solution

from hot_instance import *


class HotSolution(Solution):

	def __init__(self, inst: HotInstance, tour=None, drivers=None):
		super().__init__(inst=inst)
		self.obj_val_valid = False

		self.tour = [i for i in range(inst.n)]
		self.drivers = [0 for i in range(inst.n)]
		if tour != None:
			self.tour = tour
		if drivers != None:
			self.drivers = drivers
		

	def copy(self):
		copied_tour = [self.tour[i] for i in range(self.inst.n)]
		copied_drivers = [self.drivers[i] for i in range(self.inst.n)]
		return HotSolution(self.inst, tour=copied_tour, drivers=copied_drivers)

	def copy_from(self, other: 'HotSolution'):
		self.tour = [other.tour[i] for i in range(other.inst.n)]
		self.drivers = [other.drivers[i] for i in range(other.inst.n)]
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
		pass

	def initialize(self, k):
		pass

	def __eq__(self, other):
		pass

	def check(self):
		pass
