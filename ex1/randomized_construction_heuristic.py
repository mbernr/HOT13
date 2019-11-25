import numpy as np
import random 

from hot_instance import *
from hot_solution import *



def randomized_construction_heuristic(inst):

	tour = []
	drivers = []
	unassigned_vertices = set([i for i in range(inst.n)])

	for i in range(inst.n):
		next_vertex = random.choice(tuple(unassigned_vertices))
		tour.append(next_vertex)
		unassigned_vertices.remove(next_vertex)

	for i in range(inst.n):
		next_driver = random.randint(0, inst.k-1)
		drivers.append(next_driver)

	return HotSolution(inst, tour=tour, drivers=drivers)
