from parse import *
import numpy as np

def BeamSearch(graph, beta, V, k, L, starting_v=0):
	'''
	Input:
		graph is the graph
		V is the number of vertices
		k is the number of drivers
		L is the expected distance travelled by each driver

	Output:
		sol_basename = it returns the basename of the instance: some_prefix_n5_m8_k2_L4_1
		sol_path = a permutation of the vertices that represents the solution: 0 3 4 2 1
		sol_driver_ass = an array that describes which driver is assigned to which part 0 1 1 0 1

	How it works:
	for |V|
		- We have beta solutions in the np array "solution"
			- solution is an array of dimension beta that stores the paths i'm exploring
			- if solution is empty we just put the first point of the graph in it
		- Calculate the next vertex for all of the points in solution
		- Select the beta best points and put them in solution
	Stuff to pay attention to:
		- In neighbour calculation we need to make sure we don't use the same vertices more than once
	'''
	highnumber = 123123123123

	#set leftouts
	leftouts = set()
	for v in graph.nodes():
		leftouts.add(v)
	leftouts.remove(starting_v)

	#set solutions
	solution = {"score": highnumber, "nodes": np.full((1), starting_v), "leftouts": leftouts}
	solutions = [solution]


	for v in range(1, V):
		#calculate next nodes:
		next_step = []
		for s in solutions:
			curr = s["nodes"]
			for i in range (V):







		#for b in range(len(solution)):
		#	curr_node = []
		#	for i in range(v):
		#		curr_node = np.append(curr_node, solution[b, i])
		#		for j in range(V)
		#			if j not in
		#			curr = np.append(curr_node, )
		#			next_steps.append(curr_node)


			#calculate their score
			#pick the beta best ones
			#put them in the solution


		#else:
			#filling the first column with zero
		#	for b in range(len(solution)):
		#		solution[b, v] = reallyhighnumber #TODO think about a smart number to insert here




