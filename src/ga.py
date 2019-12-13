from hot_instance import *
from hot_solution import *
from construction_heuristics import *
import math
import sys


def ga(inst, pop_size=300, alpha=1.0, selec_ratio=0.5, repl_ratio=1.0, max_iterations=math.inf, max_time=math.inf):
	pop = initialize_pop(inst, pop_size, alpha)
	chosen_ones = select(pop, selec_ratio)
	children = crossover(chosen_ones)
	children = mutate(children)
	pop = replace(pop, children, repl_ratio)
	print(pop)
	


def initialize_pop(inst, pop_size, alpha):
	pop = []
	for _ in range(pop_size):
		pop.append(construct_random_greedy(inst, alpha))
	return pop


def select(pop, selec_ratio):
	# TODO
	# Select certain number of pop (based on selec_ratio)
	# random selection, influenced by fitness
	return pop[:round(len(pop)*selec_ratio)]


def crossover(individuals):
	# TODO
	# Take two point crossover range
	# Fill in the other stuff from the other parent in order
	return individuals 


def mutate(individuals):
	# TODO
	# tour swap (e.g. 50% chance)
	# driver fliip (e.g. 50% chance)
	# one solution can be mutated by both tour swap and driver flip
	return individuals 


def replace(pop, children, repl_ratio): # repl_ratio here?
	return pop # TODO