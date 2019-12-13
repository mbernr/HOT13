from hot_instance import *
from hot_solution import *
from construction_heuristics import *
import math
import sys
import random


def ga(inst, num_generations=math.inf, pop_size=300, alpha=1.0, selec_ratio=0.5, tour_size=3, repl_ratio=1.0, max_time=math.inf):
	'''
		repl_ratio: Maximum percentage of individuals in the new generation
	'''
	for _ in range(num_generations):
		pop = initialize_pop(inst, pop_size, alpha)
		chosen_ones = select(pop, selec_ratio, tour_size)
		children = crossover(chosen_ones)
		children = mutate(children)
		pop = replace(pop, children, repl_ratio)
		print(pop)
	


def initialize_pop(inst, pop_size, alpha):
	pop = []
	for _ in range(pop_size):
		pop.append(construct_random_greedy(inst, alpha))
	return pop


def select(pop, selec_ratio, tour_size):
	chosen = set()
	unchosen = set(range(len(pop)))
	for _ in range(round(len(pop)*selec_ratio)):
		competitors = random.sample(unchosen, tour_size)
		best = competitors[0]
		for i in range(1, len(competitors)):
			curr = competitors[i]
			if pop[curr].obj() < pop[best].obj():
				best = curr
		chosen.add(best)
		unchosen.remove(best)
	chosen_solutions = []
	for i in chosen:
		chosen_solutions.append(pop[i])
	return chosen_solutions


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