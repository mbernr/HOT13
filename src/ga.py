from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from grasp import *
from neighbourhood_structures import *
import math
import sys
import random

def ga(inst, num_generations=100, pop_size=300, using_grasp=False, alpha=1.0, selec_ratio=0.5, tour_size=3, repl_ratio=1.0, crossover_prob=0.7, mutation_prob=0.3, hof_size=3, max_time=math.inf):
	'''
		inst: instance
		num_generations = number of generations the algorithm performs
		pop_size: size of the population
		using_grasp: If true, grasp will be used for initialization. Otherwise, simple random greedy construction heuristic.
		alpha: parameter for construct_random_greedy
		selec_ratio: percentage of solutions that get selected every generation to pass their genes
		tour_size: size of the groups selected for the tournament during selection
		repl_ratio: Maximum percentage of individuals in the new generation
		crossover_prob: probability for a couple of parents to create offspring through crossover
		mutation_prob: probability that a children will be mutated
		hof_size: size of the hall of fame
		max_time: max time
	'''

	pop = initialize_pop(inst, pop_size, using_grasp, alpha)
	hof = sorted(pop, key=lambda sol: sol.obj())[:hof_size]

	for _ in range(num_generations):
		chosen_ones = select(pop, selec_ratio, tour_size)
		children = order_2p_crossover(chosen_ones, crossover_prob)
		children = mutate(children, mutation_prob)
		pop = replace(pop, children, repl_ratio)
		hof = sorted(hof + pop, key=lambda sol: sol.obj())[:hof_size]

	return hof


def initialize_pop(inst, pop_size, using_grasp, alpha):
	pop = []
	ns = TourReversal() # since we used this ns for GRASP in the first assignment
	for _ in range(pop_size):
		if using_grasp:
			pop.append(grasp(inst, ns, alpha, max_iterations=10))
		else:
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

#def randomize_2_pos(max):
#TODO
#	pos1 = random.randrange(0, len(parent1.tour), 1)
#	pos2 = random.randrange(0, len(parent1.tour), 1)
#	while pos2==pos1:
#		pos2 = random.randrange(0, len(parent1.tour), 1)
#	if pos1 > pos2:
#		pos1, pos2 = pos2, pos1
#
#	return pos1, pos2

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
	newstuff_tour = []
	newstuff_driver = []
	tour = []
	drivers = []

	for i in range(len(parent2.tour)):
		if parent2.tour[i] not in center:
			newstuff_tour.append(parent2.tour[i])
			newstuff_driver.append(parent2.drivers[i])
	
	for el in newstuff_tour[:pos1]:
		tour.append(el)
	for el in parent1.tour[pos1:pos2]:
		tour.append(el)
	for el in newstuff_tour[pos1:]:
		tour.append(el)

	for el in newstuff_driver[:pos1]:
		drivers.append(el)
	for el in parent1.drivers[pos1:pos2]:
		drivers.append(el)
	for el in newstuff_driver[pos1:]:
		drivers.append(el)

	offspring.tour = tour
	offspring.drivers = drivers

	return offspring


def order_2p_crossover(individuals, crossover_prob):
	children = []
	#go through all the parent1parent2 combinations and cross them over with a certain probability
	for pp1 in range(len(individuals)):
		for pp2 in range(len(individuals)):
			if pp1 != pp2:
				parent1 = individuals[pp1] 
				parent2 = individuals[pp2]

				if random.random() < crossover_prob:
					#with probability
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


def driver_flip(individual, pos, driver):
		individual.drivers[pos] = driver


def tour_swap(individual, p1, p2):
	individual.tour = self.reverse_array_section(individual.tour, p1, p2)
	individual.drivers = self.reverse_array_section(individual.drivers, p1, p2-1)


def mutate(children, mutation_prob):
	# tour swap (e.g. 50% chance)
	# driver flip (e.g. 50% chance)
	# one solution cannot be mutated by both tour swap and driver flip

	for child in children:
		if random.random() < mutation_prob:
			i = random.randrange(1, 2)
			if i == 1:
				pos = random.randrange(0, len(child.drivers), 1)
				driver = random.randrange(0, child.inst.k, 1)
				driver_flip(child, pos, driver)
			else:
				p1 = random.randrange(0, len(child.drivers), 1)
				p2 = random.randrange(0, len(child.drivers), 1)
				while p1 == p2 or abs(p1-p2) == (child.inst.n-1):								
					p2 = random.randrange(0, len(child.drivers), 1)
				p1, p2 = min(p1, p2), max(p1, p2)

				tour_swap(individual, p1, p2)

	return children


def replace(parents, children, repl_ratio): 

	pop_size = len(parents)
	children_needed = round(repl_ratio * pop_size)
	num_children = min(children_needed, len(children))
	num_parents = pop_size - num_children
	
	chosen_children = random.sample(children, num_children)
	chosen_parents = random.sample(parents, num_parents)

	for individual in chosen_children:
		individual.calc_objective()

	new_gen = chosen_parents + chosen_children

	return new_gen
