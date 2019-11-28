import numpy as np
import random 
import math

from hot_solution import *


### call these functions ###

def construct_greedy(inst):
	return construct(inst, rand=False)

def construct_random_greedy(inst, alpha):
	return construct(inst, rand=True, alpha=alpha)


### this makes it work ###

# Idea behind cost function for adding a vertex:
# Step 1)	select edge closest to (L*k)/n
# Step i+1)	select edge closest to (L*k - sum of weights of assigned edges) / (n - number of assigned edges) 
def cost_of_adding_vertex(inst, new_vertex, tour, tour_distance):
	total_desired_distance = inst.L*inst.k - tour_distance
	average_desired_distance = total_desired_distance / (inst.n - len(tour))
	d = inst.get_distance(tour[len(tour)-1],new_vertex)
	return abs(average_desired_distance - d)

# Idea behind cost function for adding a driver:
# Always pick the driver, that will be closest to L  
# Possible problem: Can overshoot by 50%. 
# - if overshoots by too much, then return cost + L
def cost_of_adding_driver(inst, new_driver, tour, pos, driver_dist):
	d = inst.get_distance(tour[pos],tour[(pos+1)%inst.n])
	if 1.05 * inst.L - (driver_dist + d) < 0:
		return inst.L + (driver_dist + d)
	else:
		return abs(inst.L - (driver_dist + d))


def construct(inst, rand=False, alpha=1.0):

	# starting tour with vertex 0
	tour = [0]
	unassigned_vertices = set([i for i in range(1,inst.n)])
	tour_distance = 0

	# add all vertices to tour
	while len(unassigned_vertices) > 0:

		# all unassigned vertices are candidates
		candidates = []
		for vertex in unassigned_vertices:
			candidates.append({
				"index": vertex, 
				"cost": cost_of_adding_vertex(inst, vertex, tour, tour_distance)
			})

		# selecting next vertex either greedily, or random greedily
		if rand:
			next_vertex = select_random_greedy(candidates, alpha)
		else:
			next_vertex = select_greedy(candidates)

		# update tour
		tour_distance += inst.get_distance(tour[len(tour)-1],next_vertex)
		tour.append(next_vertex)
		unassigned_vertices.remove(next_vertex)

	# starting with empty driver assignment
	drivers = []
	driver_distances = [0 for i in range(inst.k)]

	# add driver to every position
	for pos in range(inst.n):

		# all drivers are candidates
		candidates = []
		for driver in range(inst.k):
			candidates.append({
				"index": driver, 
				"cost": cost_of_adding_driver(inst, driver, tour, pos, driver_distances[driver])
			})

		# selecting next driver either greedily, or random greedily
		if rand:
			next_driver = select_random_greedy(candidates, alpha)
		else:
			next_driver = select_greedy(candidates)

		# update driver assignment
		driver_distances[next_driver] += inst.get_distance(tour[pos],tour[(pos+1)%inst.n])
		drivers.append(next_driver)

	return HotSolution(inst,tour=tour, drivers=drivers)


def select_random_greedy(candidates, alpha):
	min_cost = math.inf
	max_cost = 0
	for c in candidates:
		if c["cost"] < min_cost:
			min_cost = c["cost"]
		if c["cost"] > max_cost:
			max_cost = c["cost"]
	promising_candidates = []
	for c in candidates:
		if c["cost"] <= min_cost + alpha*(max_cost - min_cost):
			promising_candidates.append(c["index"])
	return random.choice(promising_candidates)


def select_greedy(candidates):
	min_cost = math.inf
	best_candidate = None
	for c in candidates:
		if c["cost"] < min_cost:
			min_cost = c["cost"]
			best_candidate = c["index"]
	return best_candidate

