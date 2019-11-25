import numpy as np
import random 
import math

from hot_solution import *


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
def cost_of_adding_driver(inst, new_driver, pos, tour, driver_dist):
	d = inst.get_distance(pos,(pos+1)%len(tour))
	return abs(inst.L - (driver_dist + d))


def deterministic_construction_heuristic(inst):

	# start tour with vertex 0
	tour = [0]
	unassigned_vertices = set([i for i in range(1,inst.n)])
	tour_distance = 0

	# greedily add vertices to tour
	while len(unassigned_vertices) > 0:
		min_cost = math.inf
		best_vertex = None
		for vertex in unassigned_vertices:
			cost = cost_of_adding_vertex(inst, vertex, tour, tour_distance)
			if cost < min_cost:
				best_vertex = vertex
				min_cost = cost
		tour_distance += inst.get_distance(tour[len(tour)-1],best_vertex)
		tour.append(best_vertex)
		unassigned_vertices.remove(best_vertex)

	# start with empty driver assignment
	drivers = []
	driver_distances = [0 for i in range(inst.k)]

	# greedily add drivers to tour
	for pos in range(inst.n):
		min_cost = math.inf
		best_driver = None
		for driver in range(inst.k):
			cost = cost_of_adding_driver(inst, driver, pos, tour, driver_distances[driver])
			if cost < min_cost:
				best_driver = driver
				min_cost = cost
		driver_distances[best_driver] += inst.get_distance(pos,(pos+1)%len(tour))
		drivers.append(best_driver)

	return HotSolution(inst,tour=tour, drivers=drivers)


def randomized_construction_heuristic(inst, alpha):

	# start tour with vertex 0
	tour = [0]
	unassigned_vertices = set([i for i in range(1,inst.n)])
	tour_distance = 0

	# add vertices to tour with greedy random heuristic
	while len(unassigned_vertices) > 0:

		# compute minimum and maximum cost
		min_cost = math.inf
		max_cost = 0
		for vertex in unassigned_vertices:
			cost = cost_of_adding_vertex(inst, vertex, tour, tour_distance)
			if cost < min_cost:
				min_cost = cost
			if cost > max_cost:
				max_cost = cost

		# compute restricted list of vertices 
		restricted_candidate_list = set()
		for vertex in unassigned_vertices:
			cost = cost_of_adding_vertex(inst, vertex, tour, tour_distance)
			if cost <= min_cost + alpha*(max_cost - min_cost):
				restricted_candidate_list.add(vertex)

		# select randomly from restricted list
		next_vertex = random.choice(tuple(restricted_candidate_list))

		# add selected vertex to tour and update everything
		tour_distance += inst.get_distance(tour[len(tour)-1],next_vertex)
		tour.append(next_vertex)
		unassigned_vertices.remove(next_vertex)

	# start with empty driver assignment
	drivers = []
	driver_distances = [0 for i in range(inst.k)]

	# add drivers with greedy random heuristic
	for pos in range(inst.n):

		# compute minimum and maximum cost
		min_cost = math.inf
		max_cost = 0
		for driver in range(inst.k):
			cost = cost_of_adding_driver(inst, driver, pos, tour, driver_distances[driver])
			if cost < min_cost:
				min_cost = cost
			if cost > max_cost:
				max_cost = cost

		# compute restricted list of drivers 
		restricted_candidate_list = set()
		for driver in range(inst.k):
			cost = cost_of_adding_driver(inst, driver, pos, tour, driver_distances[driver])
			if cost <= min_cost + alpha*(max_cost - min_cost):
				restricted_candidate_list.add(driver)

		# select randomly from restricted list
		next_driver = random.choice(tuple(restricted_candidate_list))

		# add selected driver and update everything
		driver_distances[next_driver] += inst.get_distance(pos,(pos+1)%len(tour))
		drivers.append(next_driver)

	return HotSolution(inst,tour=tour, drivers=drivers)


