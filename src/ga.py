from hot_instance import *
from hot_solution import *
from construction_heuristics import *
import math
import sys


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


def generate_offspring(parent1, parent2, pos1, pos2):
	'''
	parent1 and parent2 are solutions
	pos1 and pos2 are integers

	parent1 gives its elements from pos1 (included) pos2(excluded) to the offspring
	the remaining elements are inserted in the order they appear in parent2

	return the child generated
	'''
	offspring = parent1.copy()
	center = set(parent1.tour[pos1:pos2])
	newstuff = []
	for i in parent2.tour:
		if i not in center:
			newstuff.append(i)
	tour = newstuff[:pos1] + parent1.tour[pos1:pos2] +  newstuff[pos2:]
	offspring.tour = tour

	return offspring


def order_2p_crossover(individuals):
	children = []
	#go through all the parent1parent2 combinations and cross them over with a certain probability

	#randomize the two points
	#check they are not the same (otw its lame)
	#if needed swap them so pos1 < pos2
	pos1 = random.randrange(0, len(parent1.tour), 1)
	pos2 = random.randrange(0, len(parent1.tour), 1)
	while pos2==pos1:
		pos2 = random.randrange(0, len(parent1.tour), 1)
	if pos1 > pos2:
		pos1, pos2 = pos2, pos1


	#create offspring1 parent1->parent2
	offspring1 = generate_offspring(parent1, parent2, pos1, pos2)
	children.append(offspring1)

	#create offspring2 parent2->parent1
	offspring2 = generate_offspring(parent2, parent1, pos1, pos2)
	children.append(offspring2)

	return children


def mutate(individuals):
	# TODO
	# tour swap (e.g. 50% chance)
	# driver fliip (e.g. 50% chance)
	# one solution can be mutated by both tour swap and driver flip
	return individuals


def replace(pop, children, repl_ratio): # repl_ratio here?
	return pop # TODO